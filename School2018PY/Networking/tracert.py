import sys

i, o, e, = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *

sys.stdin, sys.stdout, sys.stderr = i, o, e

TTL_CONST = 11
MAX_FAIL = 10
TIMEOUT = 1
VERBOSE = 0


def main():
    """
    Receives ip and prints steps to get there
    """
    if len(sys.argv) <= 1:
        print "Wrong use of parameters. IP expected"
        return

    done = False
    step = 1
    fail_count = 0
    while not done:
        # pinging
        try:
            response = ping(sys.argv[1], step)
        except socket.gaierror:
            print "Invalid ip..."
            break
        if not response:
            # counting fails so we don't loop
            if fail_count < MAX_FAIL:
                fail_count += 1
                continue
            else:
                print "{}: no response".format(step)
                step += 1
        elif response.getlayer(ICMP).type == TTL_CONST:
            # Someone answered and it isn't the final step
            fail_count = 0
            print "{}: {}".format(step, response.getlayer(IP).src)
            step += 1
        else:
            # Someone answered and it's the final step
            print "{}: {}".format(step, response.getlayer(IP).src)
            done = True


def ping(ip, TTL):
    """
    Sends echo request to give ip with given ttl
    """
    p = IP(dst=ip, ttl=TTL) / ICMP(type="echo-request") / "Pokemon gotta catch-em-all"
    return sr1(p, verbose=VERBOSE, timeout=TIMEOUT)


if __name__ == '__main__':
    main()
