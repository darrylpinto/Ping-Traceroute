__author__ = "Darryl Pinto"

"""

This is a trace_route application that uses raw sockets to send ICMP requests
to hosts on the route to the destination host

Typing the following command will result in accessing the help menu:
    python darryl_traceroute.py

Note: Firewall may create problems in receiving packets
"""

import socket
import sys
import time

from darryl_ICMP import get_ICMP_echo


def start_trace_route(receiver, resolve_ip=True,
                      hops=30, nqueries=3, summary=False):
    """
    The Trace route method
    If the host entered does not exist, the program terminates


    :param receiver: the destination host (String)
    :param resolve_ip: If True, it resolves the IP
                        of host at the current hop (boolean)
    :param hops: maximum number of hops (int)
    :param nqueries: The number of queries per hop (int)
    :param summary: If true, it prints a summary at each hop (boolean)
    :return: None
    """
    receiver_ip = None
    payload_size = 56  # Default size
    try:
        receiver_ip = socket.gethostbyname(receiver)
    except socket.gaierror:
        print("Unable to resolve target system name %s" % receiver)
        exit(-1)

    print("Tracing route to %s {%s} over a maximum of %d hops:\n"
          % (receiver, socket.gethostbyname(receiver), hops))

    count = 1
    try:

        for i in range(1, hops+1):
            print(i, end="\t")
            sent = 0
            received = 0
            star = 0
            for j in range(nqueries):

                soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW,
                                    proto=socket.IPPROTO_ICMP)
                soc.settimeout(5)

                packet = get_ICMP_echo(payload_size, count)
                count += 1
                t1 = time.time() * 1000.0
                try:
                    soc.setsockopt(socket.SOL_IP, socket.IP_TTL, i)
                    soc.sendto(packet, (receiver, 0))
                    sent += 1
                except socket.gaierror:
                    # print("No Connection")
                    pass

                try:
                    received_data, address_tuple = soc.recvfrom(2048)
                    received += 1
                except socket.timeout:
                    print("   *   ", end="\t")
                    star += 1
                    continue

                t2 = time.time() * 1000.0
                delay = t2 - t1
                if delay > 1:
                    print("%0.f ms" % delay, end="\t")
                else:
                    print("<1 ms", end="\t")
                soc.close()

            if star == nqueries:
                print("Request Timed Out.")
            else:
                if resolve_ip:
                    try:
                        print("%s(%s)" % (
                            socket.gethostbyaddr(address_tuple[0])[0],
                            address_tuple[0]))
                    except socket.herror:
                        print(address_tuple[0])

                else:
                    print(address_tuple[0])

            if summary:
                print("\tTrace Route Statistics for %s:" % address_tuple[0])
                lost = sent - received
                print(
                    "\t\tPackets: Sent = %d, Received = %d, "
                    "Lost = %d (%d percent loss)," % (
                        sent, received, lost, 100 * lost / sent))

            if address_tuple[0] == receiver_ip:
                break

        print("\nTrace Completed")

    except KeyboardInterrupt:
        print("Interrupted")
        print("\nTrace terminated")


def main():
    """
    The main method
    :return: None
    """

    help_statement = "Usage: python darryl_traceroute.py [-n] [-q nqueries]" \
                     " [-S] [-h maxhops] target_name  \n\nOptions:\n" + \
                     "\t-n\t\tPrint hop addresses numerically" \
                     " rather than symbolically and numerically\n" + \
 \
                     "\t-q nqueries\tSet the number " \
                     "of probes per TTL to nqueries\n" + \
 \
                     "\t-S\t\tPrint a summary of how many probes were" \
                     " not answered for each hop\n" + \
 \
                     "\t-h maxhops\tSet the number of maximum hops to maxhops"

    if len(sys.argv) == 1:
        print(help_statement)

    else:
        resolve_ip = True
        nqueries = 3
        summary = False
        hops = 30

        i = 1
        while i < len(sys.argv) - 1:
            try:
                arg = sys.argv[i]
                if arg == "-n":
                    resolve_ip = False
                elif arg == "-q":
                    nqueries = int(sys.argv[i + 1])
                    i += 1
                elif arg == "-S":
                    summary = True
                elif arg == "-h":
                    hops = int(sys.argv[i + 1])
                    i += 1
                else:
                    print("Command not correct\n")
                    print(help_statement)
                    exit(-10)

                i += 1
            except ValueError:
                print("Command not correct\n")
                print(help_statement)
                exit(-10)

        receiver = sys.argv[len(sys.argv) - 1]

        start_trace_route(receiver, resolve_ip=resolve_ip,
                          nqueries=nqueries, summary=summary, hops=hops)


if __name__ == '__main__':
    main()
