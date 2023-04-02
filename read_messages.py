from src.SlackClient import SlackClient

client = SlackClient()

def read_process():
    messages = client.read_messages()
    client.save_thoughts(messages)

if __name__ == "__main__":
    messages = client.read_messages()
    client.save_thoughts(messages)
