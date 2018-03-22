''' Network module

Currently unused by the application.

TODO:
- implement high level streaming class (optional).
'''

import threading
import configparser
from time import sleep
import os


class Network(threading.Thread):
    frequency = 0.5
    timeout = 10

    def __init__(self, crawler, logger, config):
        threading.Thread.__init__(self)
        self.crawler = crawler
        self.logger = logger
        self.configure(config)

    def configure(self, config):
        self.url = config['Url']
        self.api_update = self.url + config['ApiUpdate']
        self.frequency = float(config['PostFrequency'])
        self.timeout = float(config['Timeout'])

    def run(self):
        while True:
            try:
                r = requests.post(self.api_update, data={'crawler': self.crawler.info() })
                sleep(1/self.frequency)
            except:
                self.logger.error(("Failed to POST to ", self.api_update))
                sleep(self.timeout)
