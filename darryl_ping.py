__author__ = "Darryl Pinto"

"""

This is a ping application that uses raw sockets to send ICMP echo requests
and receives reply messages.

Typing the following command will result in accessing the help menu:
    python darryl_ping.py

Note: Firewall may create problems in receiving packets
"""

import socket
import sys
import time

from darryl_ICMP import get_ICMP_echo


def check_for_timeout(timeout, start_time):
    """
    Method checks for timeout if enabled.
    It raises the TimeoutError if timeout as occured
    :param timeout: Integer representing timeout
    :param start_time: Time when the ping process started
    :return: None
    """
    if timeout is not None:
        if time.time() - start_time >= timeout:
            raise TimeoutError


def start_ping(receiver, count=0xFFFF, wait=1, payload_size=56, timeout=None):
    """
    The Ping Method.
    If the host entered does not exist, the program terminates

    :param receiver: the destination host (String)
    :param count: the number of ping requests (int)
    :param wait: The time ping needs to wait
                before sending next ping request (int)
    :param payload_size: Size of the Data Payload (int)
    :param timeout: If enabled, the program exists after timeout seconds (int)
    :return: None
    """

    start_time = None
    if timeout is not None:
        start_time = time.time()

    receiver_ip = None
    try:
        receiver_ip = socket.gethostbyname(receiver)
    except socket.gaierror:
        print("Ping request could not find host", receiver, "\nPing Terminated")
        exit(-1)

    print("Pinging %s {%s} with %d bytes of data:" % (
        receiver, str(receiver_ip), payload_size))

    soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_RAW,
                        proto=socket.IPPROTO_ICMP)
    soc.settimeout(3)
    sent = 0
    received = 0
    times = []  # To Print the Statistics

    try:

        for i in range(count):
            check_for_timeout(timeout, start_time)
            packet = get_ICMP_echo(payload_size, i)
            t1 = time.time() * 1000.0
            try:
                soc.sendto(packet, (receiver, 0))
                check_for_timeout(timeout, start_time)
            except socket.gaierror:
                # print("Connection Gone Down")
                pass

            sent += 1

            try:
                received_data, address_tuple = soc.recvfrom(2048)
            except socket.timeout:
                print("Request Timed Out")
                check_for_timeout(timeout, start_time)
                continue

            t2 = time.time() * 1000.0
            received += 1
            times.append(t2 - t1)
            print("Reply from %s: bytes=%d\ttime=%.0fms\tTTL=%d"
                  % (str(address_tuple[0]), len(received_data) - 28,
                     t2 - t1, received_data[8]))

            check_for_timeout(timeout, start_time)

            time.sleep(wait)

            check_for_timeout(timeout, start_time)

    except KeyboardInterrupt:
        print("Interrupted")

    except TimeoutError:
        print("Timeout occurred.. Stopping Ping")

    print("Ping Statistics for %s:" % (str(receiver_ip)))
    lost = sent - received
    print("    Packets: Sent = %d, Received = %d, "
          "Lost = %d (%0.2f percent loss),"
          % (sent, received, lost, 100 * lost / sent))

    print("Approximate round trip times in milli-seconds:")
    print("    Minimum = %.0fms, Maximum = %.0fms, Average = %.0fms"
          % (min(times), max(times), sum(times) / len(times)))

    soc.close()


def main():
    """
    The main method
    :return: None
    """

    help_statement = "Usage: python darryl_ping.py [-c count] [-i wait] " \
                     "[-s packetsize] [-t timeout] target_name \n" \
                     "\nOptions:\n" + \
                     "\t-c count		Stop after sending count ECHO_RESPONSE" \
                     " packets.\n\t\t\t\tIf this option is not specified, " \
                     "ping will operate until interrupted\n" + \
 \
                     "\t-i wait			Wait wait seconds between sending each " \
                     "packet.\n\t\t\t\tThe default is to wait" \
                     " for one second between each packet\n" + \
 \
                     "\t-s packetsize	\tSpecify the number of data bytes to " \
                     "be sent. The default is 56\n" + \
 \
                     "\t-t timeout		Specify a timeout, in seconds," \
                     " before ping exits\n\t\t\t\tregardless of how" \
                     " many packets have been received. Default value is None\n"

    if len(sys.argv) == 1:
        print(help_statement)
    else:
        count = 0xFFFF
        wait = 1
        packet_size = 56
        timeout = None
        i = 1
        while i < len(sys.argv) - 1:

            arg = sys.argv[i]
            try:
                if arg == "-c":
                    count = int(sys.argv[i + 1])
                    i += 1
                elif arg == "-i":
                    wait = int(sys.argv[i + 1])
                    i += 1
                elif arg == "-s":
                    packet_size = int(sys.argv[i + 1])
                    i += 1
                elif arg == "-t":
                    timeout = int(sys.argv[i + 1])
                    i += 1

                else:
                    print("Command not correct\n")
                    print(help_statement)
                    exit(-10)
                i += 1
            except ValueError:
                print("COMMAND not correct\n")
                print(help_statement)
                exit(-9)

        receiver = sys.argv[len(sys.argv) - 1]
        start_ping(receiver, count, wait, packet_size, timeout)


if __name__ == '__main__':
    main()
