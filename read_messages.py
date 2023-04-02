import os, re, datetime, requests
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import addThoughts, getLastTimestamp
from src.dropbox_client import upload_file

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
tmp_dir = "tmp"

def read_messages():
    """
    read_messages ... Function checks for the latest timestamp stored in thoughts DB
    and reads messages from specified Slack channel that are new since that timestamp.
    """
    # client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
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
    text = message["text"]
    timestamp, text = parse_time(text)
    if timestamp is None:
        timestamp = message["ts"]
    hashtags, text = parse_hashtags(text)
    files_urls = parse_attachments(message)
    text = text + ' ' + ' '.join(files_urls)
    text = text.rstrip()
    thought = {'text': text, 'timestamp_print': timestamp, 'timestamp_real': message['ts'], 'hashtags': hashtags}
    return thought

def parse_attachments(message):
    """
    parse_attachments ... Function parses attachments from message, uploads them to Dropbox and
    returns their Dropbox urls.
    """
    if "files" not in message:
        return ""
    urls = list()
    for file in message["files"]:
        file_id = file["id"]
        file_url = file['url_private_download']
        downloaded_file = download_attachment(file_id, file_url)
        url = upload_file(downloaded_file)
        urls.append(url)
        delete_tmp_file(downloaded_file)
    return urls

def download_attachment(file_id, url_private_download):
    file_info = client.files_info(file=file_id)
    headers = {"Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"}
    file_data = requests.get(url_private_download, headers=headers)
    file_path = os.path.join(tmp_dir, file_info["file"]["name"])
    with open(file_path, "wb") as f:
        f.write(file_data.content)

    return file_path

def delete_tmp_file(file_path):
    os.remove(file_path)
    

def parse_hashtags(message):
    """
    parse_hashtags ... Function parses hashtags from message text.
    """
    pattern = r'#\w+'
    hashtags = re.findall(pattern, message)
    message = re.sub(pattern, '', message)
    return hashtags, message

def parse_time(message: str):
    """
    parse_time ... Function parses time from message text.
    """
    pattern = r"\(@\s(?P<datetime>[\d.\s:]+)\)"
    match = re.search(pattern, message)
    timestamp = None
    if match:
        timestamp = create_timestamp(match.group("datetime"))
        message = re.sub(pattern, '', message)
    return timestamp, message

def create_timestamp(date_string: str):
    """
    get_timestamp ... Function creates timestamp from provided date. If no format fits, it returns None.
    """
    date_formats = ["%d. %m. %Y %H:%M", "%d. %m. %Y", "%d.%m.%Y %H:%M", "%d.%m.%Y", "%H:%M"]
    dt = None
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
    timestamp = str(dt.timestamp()) if dt is not None else None
    return timestamp

if __name__ == "__main__":
    messages = read_messages()
    save_thoughts(messages)
