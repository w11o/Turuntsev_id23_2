from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from celery_app import celery_app
from pydantic import BaseModel
import asyncio
import itertools
import hashlib
import logging
import os

app = FastAPI()
logger = logging.getLogger(__name__)

# Модель для входящих данных
class HashRequest(BaseModel):
    hash_value: str
    charset: str = "0123456789"
    max_length: int = 4

# WebSocket менеджер
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        self.active_connections[task_id] = websocket

    def disconnect(self, task_id: str):
        if task_id in self.active_connections:
            del self.active_connections[task_id]

    async def send_message(self, message: dict, task_id: str):
        if task_id in self.active_connections:
            await self.active_connections[task_id].send_json(message)

manager = ConnectionManager()

@app.post("/brut_hash")
async def create_task(request: HashRequest):
    if request.max_length > 8:
        raise HTTPException(400, "Максимальная длина не должна превышать 8 символов")
    
    # Запуск фоновой задачи
    task = celery_app.send_task(
        "bruteforce_task", 
        args=[request.hash_value, request.charset, request.max_length]
    )
    return JSONResponse({"task_id": task.id}, status_code=200)

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(websocket, task_id)
    try:
        while True:
            await websocket.receive_text()  # Для поддержания соединения
    except:
        manager.disconnect(task_id)

@app.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "status": result.status,
        "result": result.result
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
