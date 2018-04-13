import threading
import configparser
from time import sleep
import os
import json
import requests


class Network(threading.Thread):
    frequency = 10
    timeout = 10
    ip = "http://192.168.1.101:"
    port = str(3000)
    api = "/api/update/"
    message = ""

    def __init__(self, queue, message, status):
        threading.Thread.__init__(self)
        self.queue = queue
        self.message = message
        self.status = status

    def run(self):
        while True:
            try:
                self.message = str(self.queue.get())
                print('Sending POST.')
                crawler = self.status
                #print(crawler)
                r = requests.post("http://localhost:3000/api/update/", json={"crawler": crawler})
                print(r)
            except:
                print('Error sending request.')
            sleep(1/self.frequency)
        return True

