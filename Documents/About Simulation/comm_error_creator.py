import numpy
import random

def communication_error_creator_homogeneous(packet_byte_data, error_rate):  # Error is seen in all packets
    # at a ratio given with error rate. I suggested 2 similar methods for this purpose. These methods should be
    # examined with large data size to compare their speed and accuracy to represent the error.
    number_of_bytes = len(packet_byte_data)
    # Method 1 for the homogeneous error distribution
    number_of_wrong_bytes = int(number_of_bytes * error_rate)
    wrong_byte_indexes = random.sample(range(0, number_of_bytes), number_of_wrong_bytes)
    byte_data_mutable = bytearray(packet_byte_data)
    for i in wrong_byte_indexes:
        byte_data_mutable[i] = random.randint(0, 255)
    # # Method 2 for the homogeneous error distribution
    # byte_data_mutable = bytearray(packet_byte_data)
    # for i in wrong_packet_indexes:
    #     prob=random.random()
    #     if prob<error_rate:
    #         byte_data_mutable[i] = random.randint(0, 255)
    packet_byte_data = bytes(byte_data_mutable)
    return packet_byte_data


def erroneus_packet_selector(number_of_packets, error_rate):
    erroneus_packet_indexes = random.sample(range(0, number_of_packets),
                                            int(numpy.floor(number_of_packets * error_rate)))
    return erroneus_packet_indexes


def communication_error_creator_concentrated(packet_byte_data, error_rate):
    byte_data_mutable = bytearray(packet_byte_data)
    mess_ratio=0.8 # Described how much the wrong byte is randomized.
    number_of_bytes=len(packet_byte_data)
    prob_1=random.random()
    if prob_1<error_rate:
        for i in range(number_of_bytes):
            prob = random.random()
            if prob < mess_ratio:
                byte_data_mutable[i] = random.randint(0, 255)
    packet_byte_data = bytes(byte_data_mutable)
    return packet_byte_data
