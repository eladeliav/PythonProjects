import sys

i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *

sys.stdin, sys.stdout, sys.stderr = i, o, e

SRC_PORT = 1234  # source port


def receive_messages():
    """
    Constantly calls receive_message until the char is ! (exit code I decided on)
    :return:
    """
    message = "asd"
    while message != '!':
        message = receive_message()
        print message


def receive_message():
    """
    Receives a single packet and returns the char of the ascii dport
    :return: ascii version of dport
    """
    p = sniff(count=1, lfilter=lambda x: UDP in x and x[UDP].sport == SRC_PORT)
    return chr(p[0][UDP].dport)


def main():
    """
    calls receive messages
    """
    try:
        receive_messages()
    except KeyboardInterrupt:
        pass
    print "Exiting..."


if __name__ == '__main__':
    main()
