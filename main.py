import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from db.mongorest import getThoughts, addThought
import datetime


load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
# read last message in "thoughts" channel
result = client.conversations_history(channel=os.getenv("THOUGHTS_CHANNEL_ID"), inclusive=True, limit=1)
message_text = result["messages"][0]["text"]
message_timestamp = result["messages"][0]["ts"]
message_time = datetime.datetime.fromtimestamp(float(message_timestamp)).isoformat()
thought = {'text': message_text, 'time': message_time}
addThought(thought)
thoughts = getThoughts(1)
# send message to the "reminders" channel
client.chat_postMessage(channel=os.getenv("REMINDERS_CHANNEL_ID"), text=thoughts[0]["text"])
