#!/usr/bin/env python

"""Echo server using the threading API with SSL."""

import asyncio
import uuid
import ssl
from websockets import serve

connected_clients = []

async def echo(websocket):
    websocket.id = str(uuid.uuid4())
    print("CONNECT:" + websocket.id)
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            print("MESSAGE:" + websocket.id)
            for client in connected_clients:
                if client.id == websocket.id:
                    continue
                await client.send(message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("DISCONNECT:" + websocket.id)
        connected_clients.remove(websocket)

async def main():
    # Create SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    # Start the server with SSL
    async with serve(echo, "0.0.0.0", 8765, ssl=ssl_context) as server:
        await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
