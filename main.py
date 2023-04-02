from read_messages import read_process
from send_message import send_process

def do_it_all():
    """
    do_it_all ... Function runs all parts of the script at once.
    """
    read_process()
    send_process()

if __name__ == "__main__":
    do_it_all()