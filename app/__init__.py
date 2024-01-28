import os

from openai import OpenAI
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
openai_client = OpenAI()


@slack_app.message()
def message_hello(message, say):
    chat_completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message["text"]}],
    )
    say(chat_completion.choices[0].message.content)


def main():
    SocketModeHandler(slack_app, os.environ["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()
