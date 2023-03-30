import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import addThought, addThoughts, getLastTimestamp

load_dotenv()

def read_messages():
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    last_timestamp = getLastTimestamp()
    # read last messages in "thoughts" channel
    result = client.conversations_history(channel=os.getenv("THOUGHTS_CHANNEL_ID"),  oldest=last_timestamp)
    thoughts = list()
    for message in result["messages"]:
        if message["type"] == "message":
            thought = {'text': message["text"], 'timestamp': message["ts"]}
            thoughts = [thought] + thoughts
    if len(thoughts) > 0:
        addThoughts(thoughts)

if __name__ == "__main__":
    read_messages()
