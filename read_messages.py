from src.SlackClient import SlackClient

slack_client = SlackClient()

def read_process():
    messages = slack_client.read_messages()
    slack_client.save_thoughts(messages)

if __name__ == "__main__":
    read_process()
