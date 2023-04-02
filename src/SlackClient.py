import os, re, datetime, requests
from slack_sdk import WebClient
from dotenv import load_dotenv
from db.mongorest import addThoughts, getLastTimestamp, getRandomThought
from src.DropboxClient import DropboxClient

class SlackClient():
    def __init__(self):
        load_dotenv()
        self.slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        self.tmp_dir = "tmp"

    def read_messages(self):
        """
        read_messages ... Function checks for the latest timestamp stored in thoughts DB
        and reads messages from specified Slack channel that are new since that timestamp.
        """
        last_timestamp = getLastTimestamp()
        result = self.slack_client.conversations_history(channel=os.getenv("THOUGHTS_CHANNEL_ID"),  oldest=last_timestamp)
        return result["messages"]
    
    def save_thoughts(self, messages):
        """
        save_thoughts ... Function iterates through the messages and creates a dictionary of them.
        If the dictionary has at least one item, it is saved to the thoughts database.
        """
        thoughts = list()
        for message in messages:
            if "subtype" in message and message["subtype"] == "channel_join":
                continue
            thought = self.format_thought(message)
            thoughts = [thought] + thoughts
        if len(thoughts) > 0:
            addThoughts(thoughts)
    
    def format_thought(self, message):
        """
        format_thought ... Function prepares message for insertion to the thoughts database. If there
        is a date and time included in the message, it tries to parse it and use it as timestamp. If no
        date and time is provided, it uses the timestamp from Slack.
        """
        text = message["text"]
        timestamp, text = self.parse_time(text)
        if timestamp is None:
            timestamp = message["ts"]
        hashtags, text = self.parse_hashtags(text)
        text = text.rstrip()
        attachments_urls = self.parse_attachments(message)
        text = text + "\n" + attachments_urls
        thought = {'text': text, 'timestamp_print': timestamp, 'timestamp_real': message['ts'], 'hashtags': hashtags}
        return thought    

    def parse_time(self, message: str):
        """
        parse_time ... Function parses time from message text.
        """
        pattern = r"\(@\s(?P<datetime>[\d.\s:]+)\)"
        match = re.search(pattern, message)
        timestamp = None
        if match:
            timestamp = self.create_timestamp(match.group("datetime"))
            message = re.sub(pattern, '', message)
        return timestamp, message

    def create_timestamp(self, date_string: str):
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

    def parse_hashtags(self, message: str):
        """
        parse_hashtags ... Function parses hashtags from message text.
        """
        pattern = r'#\w+'
        hashtags = re.findall(pattern, message)
        message = re.sub(pattern, '', message)
        return hashtags, message
    
    def parse_attachments(self, message):
        """
        parse_attachments ... Function parses attachments from message, uploads them to Dropbox and
        returns their Dropbox urls.
        """
        if "files" not in message:
            return ""
        urls = list()
        dropbox_client = DropboxClient()
        for file in message["files"]:
            file_id = file["id"]
            file_url = file['url_private_download']
            downloaded_file = self.download_attachment(file_id, file_url)
            url = dropbox_client.upload_file(downloaded_file)
            urls.append(url)
            self.delete_tmp_file(downloaded_file)
        urls_prepared = "\n".join(urls)
        return urls_prepared.strip()

    def download_attachment(self, file_id, url_private_download):
        """
        download_attachment ... Function downloads attachment from Slack, saves it in tmp directory
        and returns path to the saved file.
        """
        file_info = self.slack_client.files_info(file=file_id)
        headers = {"Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"}
        file_data = requests.get(url_private_download, headers=headers)
        file_path = os.path.join(self.tmp_dir, file_info["file"]["name"])
        with open(file_path, "wb") as f:
            f.write(file_data.content)
        return file_path

    def delete_tmp_file(self, file_path):
        """
        delete_tmp_file ... Function deletes temporary file acording to provided path.
        """
        os.remove(file_path)
    
    def prepare_mesage(self):
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

    def send_message(self, message):
        """
        send_message ... Function sends message in the specified Slack channel.
        """
        self.slack_client.chat_postMessage(channel=os.getenv("REMINDERS_CHANNEL_ID"), text=message)