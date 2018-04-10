from streaming_server import StreamingServer


address = ('', 8080)
server = StreamingServer()

server.connect()
server.serve_forever(0.5)
