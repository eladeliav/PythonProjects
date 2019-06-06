import sys

i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *

sys.stdin, sys.stdout, sys.stderr = i, o, e


def include_dns(p):
    return Raw in p and str(p[Raw]).startswith('GET')


def main():
    packets = sniff(count=1, lfilter=include_dns)
    for p in packets:
        print "Raw: " + str(p[Raw])


if __name__ == '__main__':
    main()
