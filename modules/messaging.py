import threading


class OutboundMessaging(threading.Thread):
    message = ""

        def __init__(self, port, frequency, message):
            threading.Thread.__init__(self)
            self.port = port
            self.frequency = frequency
            self.message = message

        def run(self):
            while True:
                try:
                    self.port.write(self.message.encode())
                except:
                    print("Outbound messaging stopped working.")
                sleep(1/self.frequency)
            return True

        def set_message(self, message):
            this.message = message
            return True



class InboundMessaging(threading.Thread):
    read_size = 128
    message = ""

        def __init__(self, port, frequency, message):
            threading.Thread.__init__(self)
            self.port = port
            self.frequency = frequency
            self.message = message

        def run(self):
            while True:
                try:
                    self.message = self.port.read(self.read_size)
                except:
                    print("Inbound message not recieved.")
                sleep(1/self.frequency)
            return True

        def get_message(self):
            return this.message
