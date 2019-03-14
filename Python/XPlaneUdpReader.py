import struct
import socket
import time

from XPlaneMessage import XPlaneMessage

Address = "127.0.0.1"
Port = 8088
BufferSize = 4096


def generate_file_name():
    return str(int(time.time())) + ".txt"


def write_messages_to_file(messages, file):
    # data order is pitch roll heading altitude speed throttle elevation aileron rudder
    file.write(f'{messages[17].Values[0]} {messages[17].Values[1]} {messages[17].Values[2]} {messages[20].Values[3]} {messages[3].Values[0]} {messages[25].Values[0]} {messages[8].Values[0]} {messages[8].Values[1]} {messages[8].Values[2]}\n')


def start_program():
    xplane_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    xplane_socket.bind((Address, Port))
    file_name = generate_file_name()
    file = open(file_name, "w", buffering=128)
    while True:
        data, address = xplane_socket.recvfrom(BufferSize)
        header = struct.unpack('4s', data[0:4])[0].decode('utf-8')
        if header == 'DATA':
            messages = parse_messages(data[5:])
            write_messages_to_file(messages, file)
            print(f'{len(messages)} messages are parsed!')


def parse_messages(message_bytes):
    total_byte = len(message_bytes)
    start_byte = 0
    messages = {}
    while start_byte < total_byte:
        message_end_byte = start_byte + 36
        data_bytes = message_bytes[start_byte:message_end_byte]
        message = byte2message(data_bytes)
        messages[message.Id] = message
        start_byte += 36
    return messages


def byte2message(data_bytes):
    message = XPlaneMessage()
    data = struct.unpack('i8f', data_bytes)
    message.Id = data[0]
    message.Values = [data[i] for i in range(1, 9)]
    return message


if __name__ == '__main__':
    start_program()
