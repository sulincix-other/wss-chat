import http.server
import ssl

# Define the server address and port
server_address = ('0.0.0.0', 4443)  # Listen on all interfaces

# Create a simple HTTP server
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

# Wrap the server socket with SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://0.0.0.0:4443")
httpd.serve_forever()
