import os
from time import sleep

import requests
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta import Assistant
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = OpenAI()
assistant: Assistant | None = None

MODEL = "gpt-3.5-turbo-1106"


@app.message()
def handle_message(message, say):
    chat_completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": message["text"]}],
    )
    say(chat_completion.choices[0].message.content)


@app.event({"type": "message", "subtype": "file_share"})
def handle_message_file_share(body, say):
    global assistant
    file = body["event"]["files"][0]
    file_url = file["url_private"]
    file_name = file["name"]
    file_data = bytearray()
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    with requests.get(file_url, headers=headers, stream=True) as response:
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=8192):
                file_data.extend(chunk)
            file_content = bytes(file_data)
            text_content = file_content.decode("utf-8")
            say(
                f'You sent me the file "{file_name}" with contents "{text_content}". Uploading to OpenAI...'
            )
        else:
            say(
                'You tried to send me the file "{file_name}" but I could not access it.'
            )
            return
    file = client.files.create(file=file_content, purpose="assistants")
    if assistant is None:
        say("Finding OpenAI document assistant...")
        assistants = client.beta.assistants.list()
        for a in assistants:
            if a.name == "Document Assistant":
                assistant = a
                break
        if assistant is None:
            say("Document assistant not found, creating...")
            assistant = client.beta.assistants.create(
                name="Document Assistant",
                instructions="You are a helpful assistant that answers questions about documents.",
                model=MODEL,
                tools=[{"type": "retrieval"}],
            )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Summarize this file.",
                "file_ids": [file.id],
            }
        ]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id
    )
    run_id = run.id
    status = run.status
    say(f"Summarizing... {status}")
    while status == "queued" or status == "in_progress":
        sleep(1)
        run = client.beta.threads.runs.retrieve(run_id=run_id, thread_id=thread.id)
        if run.status != status:
            status = run.status
            say(f"Summarizing... {status}")
    if status != "completed":
        say("Sorry, I could not summarize that file.")
        return
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    content = messages.data[0].content[0]
    if content.type != "text":
        say(f"OpenAI sent {content.type}.")
        return

    # Extract the message content
    # https://platform.openai.com/docs/assistants/how-it-works/message-annotations
    message_content = content.text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f" [{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(
                f"[{index}] {file_citation.quote} from {cited_file.filename}"
            )
        elif file_path := getattr(annotation, "file_path", None):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f"[{index}] from {cited_file.filename}")
    message_content.value += "\n" + "\n".join(citations)

    say(message_content.value)


def main():
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()


if __name__ == "__main__":
    main()
