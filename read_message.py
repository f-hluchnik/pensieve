import os
import sys
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import addThought
import datetime

sys.path.append("..")
load_dotenv()

def read_message():
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    # read last message in "thoughts" channel
    result = client.conversations_history(channel=os.getenv("THOUGHTS_CHANNEL_ID"), inclusive=True, limit=1)
    message_text = result["messages"][0]["text"]
    message_timestamp = result["messages"][0]["ts"]
    message_time = datetime.datetime.fromtimestamp(float(message_timestamp)).isoformat()
    thought = {'text': message_text, 'time': message_time}
    addThought(thought)

if __name__ == "__main__":
    read_message()
