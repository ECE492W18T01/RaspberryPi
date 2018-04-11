''' Network module

Currently unused by the application.

TODO:
- implement high level streaming class (optional).
'''

import threading
import configparser
from time import sleep
import os
import json
import requests


class Network(threading.Thread):
    frequency = 0.5
    timeout = 10
    ip = "http://192.168.1.101:"
    port = str(3000)
    api = "/api/update/"

    def __init__(self):
        threading.Thread.__init__(self)
        

    def set_message(self, message):
        self.message = str(message)
        return True

    def run(self):
        #print('Payload: ' + self.message)
        r = requests.post("http://localhost:3000/api/update/", json={"crawler": self.message})
        print(r)
        return True
