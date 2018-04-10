from http import server

class StreamingHandler(server.BaseHTTPRequestHandler):

    def set_stream(stream):
        this.stream = stream

    def do_GET(self):
        if self.path == '/index.html':
            content = "Hello".encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        if self.path == '/stream.mjpeg':
            print('Stream request')
            self.send_response(200)
            #self.send_header('Age', 0)
            #self.send_header('Cache-Control', 'no-cache, private')
            #self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=--FRAME')
            self.end_headers()

            try:

                while True:
                    print('.')
                    with this.stream.condition:
                        this.stream.condition.wait()
                        frame = this.stream.frame
                    print('Frame available')
                    #print(frame)
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    print(self)
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
