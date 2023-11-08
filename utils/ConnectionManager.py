from fastapi import WebSocket

class Manager:
    def __init__(self):
        self.conns: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.conns.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.conns.remove(websocket)
        
    async def broadcast(self, config):
        for ws in self.conns:
            await ws.send_json(config)