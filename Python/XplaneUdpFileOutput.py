import os
import time

from XPlaneUdpReader import XPlaneUdpReader

udp_reader: XPlaneUdpReader = XPlaneUdpReader.get_instance()
folder = "takeoff/"


def generate_file_name():
    if not os.path.isdir(folder):
        os.mkdir(folder)
    return folder + str(int(time.time())) + ".txt"


output_file_name = generate_file_name()
output_file = open(output_file_name, "w", )


def write2file(messages):
    # data order is : pitch roll heading altitude speed throttle elevation aileron rudder
    output_file.write(
        f'{messages[17].Values[0]} {messages[17].Values[1]} {messages[17].Values[2]} {messages[20].Values[3]} '
        f'{messages[3].Values[0]} {messages[25].Values[0]} {messages[8].Values[0]} {messages[8].Values[1]} '
        f'{messages[8].Values[2]}\n')


udp_reader.add_listener(write2file)
udp_reader.start()
