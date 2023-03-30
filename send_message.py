import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import getThoughts

load_dotenv()

def send_message():
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    thoughts = getThoughts(1)
    # send message to the "reminders" channel
    client.chat_postMessage(channel=os.getenv("REMINDERS_CHANNEL_ID"), text=thoughts[0]["text"])

if __name__ == "__main__":
    send_message()
