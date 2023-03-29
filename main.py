import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
# read last message in "thoughts" channel
result = client.conversations_history(channel=os.getenv("THOUGHTS_CHANNEL_ID"), inclusive=True)
message_text = result["messages"][0]["text"]
# send message to the "reminders" channel
client.chat_postMessage(channel=os.getenv("REMINDERS_CHANNEL_ID"), text=message_text)
