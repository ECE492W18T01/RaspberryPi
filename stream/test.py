import io
import time
import picamera
from PIL import Image

stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')

stream.seek(0)
image = Image.open(stream)