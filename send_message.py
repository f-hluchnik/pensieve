import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import getRandomThought, getThoughts
import datetime

load_dotenv()

def prepare_mesage():
    """
    prepare_message ... Function retrieves random thought from thoughts database and formats it.
    """
    random_thought = getRandomThought()
    ## Code for getting one thought, mainly for testing purposes.
    # random_thoughts = getThoughts()
    # if len(random_thoughts) == 0:
    #     return "Nothing found."
    # random_thought = random_thoughts[0]
    thought = random_thought["text"]
    time = datetime.datetime.fromtimestamp(float(random_thought["timestamp_print"])).strftime("%a, %d. %m. %Y, %H:%M")
    message = thought + "\n(" + time + ")"
    return message

def send_message(message):
    """
    send_message ... Function sends message in the specified Slack channel.
    """
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    client.chat_postMessage(channel=os.getenv("REMINDERS_CHANNEL_ID"), text=message)

if __name__ == "__main__":
    message = prepare_mesage()
    send_message(message)
