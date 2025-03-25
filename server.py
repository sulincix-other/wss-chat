#!/usr/bin/env python3

# Python 3 server
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import ssl
import os

hostName = "0.0.0.0"
serverPort = 4443

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path.startswith("/audio"):
            with open("audio.html","rb") as f:
                self.wfile.write(f.read())
        else:
            with open("message.html","rb") as f:
                self.wfile.write(f.read())

httpd = HTTPServer((hostName, serverPort), Server)

if os.path.isfile("cert.pem") and os.path.isfile("key.pem"):
    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    # Wrap the server socket with SSL
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://0.0.0.0:4443")
httpd.serve_forever()
