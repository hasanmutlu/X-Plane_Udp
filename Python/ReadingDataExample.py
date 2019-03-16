from XPlaneUdpReader import XPlaneUdpReader

udp_reader = XPlaneUdpReader.get_instance()
udp_reader.add_listener(lambda x: print(x))
udp_reader.start()
