import uuid
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse

from db import init_db, add_session, remove_session, get_all_sessions
from models import Session

app = FastAPI()
init_db()

connected_clients = []


@app.get("/")
async def get_index(request: Request):
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    session_id = str(uuid.uuid4())

    await websocket.send_json({"action": "set_session_id", "session_id": session_id})

    try:
        while True:
            data = await websocket.receive_json()
            if data["action"] == "connect":
                session = Session(
                    session_id=session_id,
                    start_time=datetime.now(),
                    user_agent=data["user_agent"],
                    ip=websocket.client.host
                )
                add_session(session)
                await sync_sessions()

            elif data["action"] == "disconnect":
                session_id = data["session_id"]
                remove_session(session_id)
                await sync_sessions()

    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def sync_sessions():
    sessions = get_all_sessions()
    for client in connected_clients:
        await client.send_json({"action": "update", "sessions": sessions})
