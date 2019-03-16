import time

from FlightControl import FlightControl
from XPlaneUdpWriter import XPlaneUdpWriter

f = FlightControl()
f.throttle = 1
f.elevation = 0.5

while True:
    writer = XPlaneUdpWriter.get_instance().send_messages(f.get_udp_messages())
    time.sleep(1)
