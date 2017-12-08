__author__ = "Darryl Pinto"

"""
This program contains the method to create a ICMP echo packet.
The ping and traceroute applications import
get_ICMP_echo method to create ICMP packets
"""

import random
import struct


def get_checksum(data):
    """
    Get the checksum of the packet.
    Checksum is calculated as stated in RFC 792
    :param data: list in bytes to calculate the checksum
    :return: 16 bit checksum of the packet
    """
    one_complement_sum = 0
    odd = 1
    if len(data) % 2 == 0:
        odd = 0

    for i in range(0, len(data) - odd, 2):

        # For shifting 8 bits
        first = (data[i] << 8)
        second = data[i + 1]
        one_complement_sum += first + second

        if one_complement_sum > 65535:
            one_complement_sum &= 0xFFFF  # carry
            one_complement_sum += 1

    if odd:
        one_complement_sum += (data[len(data) - 1] << 8)
        if one_complement_sum > 65535:
            one_complement_sum &= 0xFFFF  # carry
            one_complement_sum += 1

    one_complement_sum ^= 0xFFFF
    return one_complement_sum


def get_ICMP_echo(payload_size, seq):
    """
    Method to create the ICMP  echo (Type = 8) packet
    :param payload_size: Size of the Data Payload
    :param seq: The current Sequence Number of the Packet
    :return: ICMP packet in bytes
    """
    icmp_type = 8
    icmp_code = 0
    init_checksum = 0
    icmp_id = random.randint(0, 0xFFFF)
    icmp_seq = seq
    _checksum = struct.pack("!BBHHH", icmp_type, icmp_code, init_checksum,
                            icmp_id, icmp_seq)

    payload = ""
    for i in range(payload_size):
        payload += 'a'
    payload = bytes(payload, 'utf-8')

    icmp_checksum = get_checksum(_checksum + payload)

    header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum,
                         icmp_id, icmp_seq)

    return header + payload


