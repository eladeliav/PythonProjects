import sys

i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *

sys.stdin, sys.stdout, sys.stderr = i, o, e

MIN_PORT_RANGE = 77
MAX_PORT_RANGE = 85

def main():
    """
    Checks what ports are open in a given port range and ip
    """
    open_ports = []

    ip = raw_input("give ip")

    for x in range(MIN_PORT_RANGE, MAX_PORT_RANGE):
        p = syn_ack(437, ip, x)
        ans = sr1(p, timeout=1, verbose=False)
        if ans:
            open_ports.append(x)
    print open_ports


def syn_ack(s, ip, port):
    """
    creates syn packet to given ip and port
    """
    return IP(dst=ip) / TCP(dport=port, flags='S', seq=s)


if __name__ == '__main__':
    main()
