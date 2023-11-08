from fastapi import WebSocket
from pydantic import BaseModel

class Config(BaseModel):
    user_pass: str
    texto: str
    cor_fonte: str
    cor_fundo: str
    anim: str
    tempo_segundos: str

class Manager:
    def __init__(self):
        self.conns: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.conns.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.conns.remove(websocket)
        
    async def broadcast(self, config: Config):
        for ws in self.conns:
            await ws.send_json(config)