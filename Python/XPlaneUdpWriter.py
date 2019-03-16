import socket
import struct

from XPlaneMessage import XPlaneMessage


class XPlaneUdpWriter:
    Address = "127.0.0.1"
    Port = 49000
    __instance__ = None

    @staticmethod
    def get_instance():
        if XPlaneUdpWriter.__instance__ is None:
            XPlaneUdpWriter()
        return XPlaneUdpWriter.__instance__

    def __init__(self):
        if self.__instance__ is not None:
            raise Exception('This class is Singleton!')
        else:
            self.xplane_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            XPlaneUdpWriter.__instance__ = self

    @staticmethod
    def messages2bytes(messages):
        if type(messages) == XPlaneMessage:
            messages = [messages]
        msg_byte = struct.pack('<5s', b'DATA\0')
        for i in range(0, len(messages)):
            message: XPlaneMessage = messages[i]
            msg_byte += struct.pack('<i8f', message.Id, *message.Values)
        return msg_byte

    def send_bytes(self, data):
        self.xplane_socket.sendto(data, (XPlaneUdpWriter.Address, XPlaneUdpWriter.Port))

    def send_messages(self, messages):
        data = XPlaneUdpWriter.messages2bytes(messages)
        self.send_bytes(data)
