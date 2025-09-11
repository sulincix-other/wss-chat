import uuid

import traceback

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

###### html routes ######

with open("pages/message.html") as f:
    message = f.read()

with open("pages/audio.html") as f:
    audio = f.read()

@app.get("/")
async def get_msg():
    return HTMLResponse(message)

@app.get("/audio")
async def get_audio():
    return HTMLResponse(audio)

@app.get("/{channel}")
async def get_msg2():
    return HTMLResponse(message)

@app.get("/audio/{channel}")
async def get_audio2():
    return HTMLResponse(audio)


###### websocket ######
connected_clients = {}

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket):
    path = websocket.url.path
    websocket.id = str(uuid.uuid4())
    print(f"CONNECT: {path}: {websocket.id}")

    if path not in connected_clients:
        connected_clients[path] = []
    connected_clients[path].append(websocket)

    await websocket.accept()

    try:
        while True:
            isb = False # is bytes
            try:
                data = await websocket.receive_bytes()
                isb = True
            except:
                data = await websocket.receive_text()
            print(f"MESSAGE: {path}: {websocket.id} - {data}")
            for client in connected_clients[path]:
                if client.id != websocket.id:
                    if isb:
                        await client.send_bytes(data)
                    else:
                        await client.send_text(data)
    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
    finally:
        print(f"DISCONNECT: {path}: {websocket.id}")
        connected_clients[path].remove(websocket)
        if not connected_clients[path]:
            del connected_clients[path]

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

if __name__ == "__main__":
    main()
