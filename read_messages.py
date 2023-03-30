import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import addThoughts, getLastTimestamp

load_dotenv()

def read_messages():
    """
    read_messages ... Function checks for the latest timestamp stored in thoughts DB
    and reads messages from specified Slack channel that are new since that timestamp.
    """
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    last_timestamp = getLastTimestamp()
    result = client.conversations_history(channel=os.getenv("THOUGHTS_CHANNEL_ID"),  oldest=last_timestamp)
    return result["messages"]

def save_thoughts(messages):
    """
    save_thoughts ... Function iterates through the messages and creates a dictionary of them.
    If the dictionary has at least one item, it is saved to the thoughts database.
    """
    thoughts = list()
    for message in messages:
        if message["type"] == "message":
            thought = {'text': message["text"], 'timestamp': message["ts"]}
            thoughts = [thought] + thoughts
    if len(thoughts) > 0:
        addThoughts(thoughts)

if __name__ == "__main__":
    messages = read_messages()
    save_thoughts(messages)
