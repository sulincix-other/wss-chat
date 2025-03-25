#!/usr/bin/env python

"""Echo server using the threading API with SSL."""

import os
import asyncio
import uuid
import ssl
from websockets import serve

from server import run
import threading

connected_clients = {}

async def echo(websocket):
    path = websocket.request.path
    websocket.id = str(uuid.uuid4())
    print("CONNECT:{}:{}".format(path, websocket.id))
    if path not in connected_clients:
        connected_clients[path] = []
    connected_clients[path].append(websocket)
    try:
        async for message in websocket:
            print("MESSAGE:{}:{}".format(path, websocket.id))
            for client in connected_clients[path]:
                if client.id == websocket.id:
                    continue
                await client.send(message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("DISCONNECT:{}:{}".format(path, websocket.id))
        connected_clients[path].remove(websocket)

async def main():
    if os.path.isfile("cert.pem") and os.path.isfile("key.pem"):
        # Create SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        # Start the server with SSL
        async with serve(echo, "0.0.0.0", 8765, max_size=None, ssl=ssl_context) as server:
            await server.wait_closed()
    else:
        async with serve(echo, "0.0.0.0", 8765, max_size=None) as server:
            await server.wait_closed()

if __name__ == "__main__":
    threading.Thread(target=run).start()
    asyncio.run(main())
