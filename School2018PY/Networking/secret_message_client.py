import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *

sys.stdin, sys.stdout, sys.stderr = i, o, e

DST_IP = "0.0.0.0"  # destination ip
SRC_PORT = 1234  # source port


def main():
    """
    calls send_messages()
    """
    try:
        send_messages()
    except KeyboardInterrupt:
        pass
    print "Exiting..."


def send_messages():
    """
    Asks for input and sends it to the dst_ip as separate packets for each char
    and in ascii form
    """
    user_input = raw_input("> ")
    while user_input.upper() != "QUIT":
        for letter in user_input:
            letter = ord(letter)
            p = IP(dst=DST_IP) / UDP(sport=SRC_PORT, dport=letter)
            print "Sending empty message on port " + str(letter)
            send(p)
        user_input = raw_input("> ")


if __name__ == '__main__':
    main()
