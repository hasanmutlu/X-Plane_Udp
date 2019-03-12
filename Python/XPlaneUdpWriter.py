import socket
import struct
import time

from XPlaneMessage import XPlaneMessage


def messages2bytes(messages):
    if type(messages) == XPlaneMessage:
        messages = [messages]
    msg_byte = struct.pack('<5s', b'DATA\0')
    for i in range(0, len(messages)):
        message: XPlaneMessage = messages[i]
        msg_byte += struct.pack('<i8f', message.Id, *message.Values)
    return msg_byte


def start_program():
    # test program
    values = [float(1) for i in range(0, 8)]
    message = XPlaneMessage()
    message.Id = 25
    message.Values = values
    data = messages2bytes(message)
    print(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    while True:
        sock.sendto(data, ('127.0.0.1', 49000))
        time.sleep(1)


if __name__ == '__main__':
    start_program()
