from read_messages import read_messages, save_thoughts
from send_message import send_message, prepare_mesage

def do_it_all():
    """
    do_it_all ... Function runs all parts of the script at once.
    """
    messages = read_messages()
    save_thoughts(messages)
    message = prepare_mesage
    send_message(message)

if __name__ == "__main__":
    do_it_all()