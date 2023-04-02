from src.SlackClient import SlackClient

slack_client = SlackClient()

def send_process():
    message = slack_client.prepare_mesage()
    slack_client.send_message(message)

if __name__ == "__main__":
    send_process()
