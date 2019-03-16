from XPlaneMessage import XPlaneMessage


class FlightControl:
    def __init__(self):
        self.throttle = float(0)
        self.elevation = float(0)
        self.aileron = float(0)
        self.rudder = float(0)

    def __get_throttle_message(self):
        throttle_message = XPlaneMessage()
        throttle_message.Id = 25
        throttle_message.Values = [self.throttle] * 8
        return throttle_message

    def __get_control_message(self):
        control_message = XPlaneMessage()
        control_message.Id = 8
        control_message.Values[0] = self.elevation
        control_message.Values[1] = self.aileron
        control_message.Values[2] = self.rudder
        return control_message

    def get_udp_messages(self):
        messages = list()
        messages.append(self.__get_throttle_message())
        messages.append(self.__get_control_message())
        return messages
