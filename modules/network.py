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


class Network(threading.Thread):
    frequency = 0.5
    timeout = 10
    ip = "http:192.168.1.101:"
    port = 3000
    api = "/api/update/"

    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.api_url = self.ip + self.port + self.api

    def configure(self, config):
        self.url = config['Url']
        self.api_update = self.url + config['ApiUpdate']
        self.frequency = float(config['PostFrequency'])
        self.timeout = float(config['Timeout'])

    def set_message(self, message):
        self.message = message
        return True

    def run(self):
        try:
            print('Starting network call..')
            print('Payload: ' + self.message)
            r = requests.post(self.api_url, data={'crawler': self.message})
            print(r)
        except:
            print("Failed to POST to ", self.api_update)
            self.logger.error(("Failed to POST to ", self.api_update))
        return True
