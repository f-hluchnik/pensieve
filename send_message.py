from src.SlackClient import SlackClient

client = SlackClient()

def send_process():
    message = client.prepare_mesage()
    client.send_message(message)

if __name__ == "__main__":
    message = client.prepare_mesage()
    client.send_message(message)
