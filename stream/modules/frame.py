from threading import Condition

class Frame(object):

    def __init__(self):
        self.frame = None
        self.length = 0
        self.condition = Condition()

    def write_frame(self, frame):
        with self.condition:
            self.frame = frame
            self.condition.notify_all()
        return True

    def get_frame(self):
        return self.frame

    def wait_for_new_frame(self):
        with this.condition:
            this.condition.wait()
            return this.frame

    def save_frame_as_jpeg(self, path):
        f = open(path, "wb")
        f.write(self.frame)
        f.close()
