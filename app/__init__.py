import os

import requests
from dotenv import load_dotenv
from openai import OpenAI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
openai_client = OpenAI()


@app.message()
def handle_message(message, say):
    chat_completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message["text"]}],
    )
    say(chat_completion.choices[0].message.content)


@app.event({"type": "message", "subtype": "file_share"})
def handle_message_file_share(body, say):
    file = body["event"]["files"][0]
    file_url = file["url_private"]
    file_name = file["name"]
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    with requests.get(file_url, headers=headers, stream=True) as response:
        if response.status_code == 200:
            file_data = bytearray()
            for chunk in response.iter_content(chunk_size=8192):
                file_data.extend(chunk)
            file_content = bytes(file_data)
            text_content = file_content.decode("utf-8")
            say(f'You sent me the file "{file_name}" with contents "{text_content}"')
        else:
            say('You tried to send me the file "{file_name}" but I could not access it')


def main():
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()


if __name__ == "__main__":
    main()
