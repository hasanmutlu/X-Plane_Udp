import struct
import socket

from XPlaneMessage import XPlaneMessage

Address = "127.0.0.1"
Port = 8088
BufferSize = 4096


def start_program():
    xplane_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    xplane_socket.bind((Address, Port))
    while True:
        data, address = xplane_socket.recvfrom(BufferSize)
        header = struct.unpack('4s', data[0:4])[0].decode('utf-8')
        if header == 'DATA':
            messages = parse_messages(data[5:])
            print(f'{len(messages)} messages are parsed!')


def parse_messages(message_bytes):
    total_byte = len(message_bytes)
    start_byte = 0
    messages = []
    while start_byte < total_byte:
        message_end_byte = start_byte + 36
        data_bytes = message_bytes[start_byte:message_end_byte]
        message = byte2message(data_bytes)
        print(str(message))
        messages.append(message)
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
