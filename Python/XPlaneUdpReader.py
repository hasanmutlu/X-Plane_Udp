import struct
import socket
from inspect import signature
from threading import Thread
from XPlaneMessage import XPlaneMessage


class XPlaneUdpReader(Thread):
    Address = "127.0.0.1"
    Port = 8088
    BufferSize = 4096
    __instance__ = None

    @staticmethod
    def get_instance():
        if XPlaneUdpReader.__instance__ is None:
            XPlaneUdpReader()
        return XPlaneUdpReader.__instance__

    def __init__(self):
        if self.__instance__ is not None:
            raise Exception('This class is Singleton!')
        else:
            super(XPlaneUdpReader, self).__init__()
            self.__listener_list__ = []
            self.xplane_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.xplane_socket.bind((self.Address, self.Port))
            XPlaneUdpReader.__instance__ = self

    def add_listener(self, listener):
        if callable(listener) and listener not in self.__listener_list__:
            if len(signature(listener).parameters) == 1:
                self.__listener_list__.append(listener)
            else:
                print("Given listener function should have 1 parameters as XPlaneMessage")
        else:
            print("Only functions can be added as listener!!")

    @staticmethod
    def byte2message(data_bytes):
        message = XPlaneMessage()
        data = struct.unpack('i8f', data_bytes)
        message.Id = data[0]
        message.Values = [data[i] for i in range(1, 9)]
        return message

    @staticmethod
    def parse_messages(message_bytes):
        total_byte = len(message_bytes)
        start_byte = 0
        messages = {}
        while start_byte < total_byte:
            message_end_byte = start_byte + 36
            data_bytes = message_bytes[start_byte:message_end_byte]
            message = XPlaneUdpReader.byte2message(data_bytes)
            messages[message.Id] = message
            start_byte += 36
        return messages

    def start(self):
        if self.is_alive():
            print("XPlaneUdpReader is already running!")
        else:
            super(XPlaneUdpReader, self).start()

    def run(self):
        while True:
            data, address = self.xplane_socket.recvfrom(self.BufferSize)
            header = struct.unpack('4s', data[0:4])[0].decode('utf-8')
            if header == 'DATA':
                messages = self.parse_messages(data[5:])
                # call all listeners and pass messages to them
                [self.__listener_list__[i](messages) for i in range(0, len(self.__listener_list__))]


XPlaneUdpReader.get_instance().start()
