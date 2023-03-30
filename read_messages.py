import os, re, datetime
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
        if "subtype" not in message or message["subtype"] != "channel_join":
            thought = format_thought(message)
            thoughts = [thought] + thoughts
    if len(thoughts) > 0:
        addThoughts(thoughts)

def format_thought(message):
    """
    format_thought ... Function prepares message for insertion to the thoughts database. If there
    is a date and time included in the message, it tries to parse it and use it as timestamp. If no
    date and time is provided, it uses the timestamp from Slack.
    """
    timestamp = message["ts"]
    pattern = r"\(\#datetime\s(?P<datetime>[\d.\s:]+)\)"
    match = re.search(pattern, message["text"])
    if match:
        timestamp = get_timestamp(match.group("datetime")) or message["ts"]

    thought = {'text': message["text"], 'timestamp': str(timestamp)}
    return thought

def get_timestamp(date_string):
    """
    get_timestamp ... Function tries to parse date and time from the message. It tries several
    date and time formats. If no format fits, it returns 0.
    """
    date_formats = ["%d. %m. %Y %H:%M", "%d. %m. %Y", "%d.%m.%Y %H:%M", "%d.%m.%Y", "%H:%M"]
    for format_code in date_formats:
        try:
            if format_code == "%H:%M":
                today = datetime.date.today()
                time = datetime.datetime.strptime(date_string, format_code).time()
                dt = datetime.datetime.combine(today, time)
            else:
                dt = datetime.datetime.strptime(date_string, format_code)
            break
        except ValueError:
            pass
    if dt is not None:
        timestamp = dt.timestamp()
    else:
        timestamp = 0
    return timestamp

if __name__ == "__main__":
    messages = read_messages()
    save_thoughts(messages)
