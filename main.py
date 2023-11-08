from typing import Annotated
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status #Path e Query ajudam a documentação e validação automática
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware

from utils.templatesRender import Render
from utils.ConnectionManager import Manager

class Config(BaseModel):
    texto: str = 'Exemplo'
    cor_fonte: str = '#0000ff'
    cor_fundo: str = '#cccccc'
    anim: str = 'slide'
    tempo_segundos: str = '10'
    
config_default = Config().model_dump()

websocket_list = Manager()

app = FastAPI()

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
    # exposed_headers= HEADERS,
)

@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(content=Render('index.html'), status_code=200)

@app.get('/criar/{user_name}')
def edit(user_name: str):
    return HTMLResponse(content=Render('criar.html', {'user_name':user_name.lower()}), status_code=200)

@app.get('/logar/{user_name}')
def logar(user_name: str):
    return HTMLResponse(content=Render('logar.html', {'user_name':user_name.lower()}), status_code=200)

@app.websocket("/ws/{user_name}")
async def websocket_endpoint(websocket: WebSocket, user_name: str):
    await websocket_list.connect(websocket, user_name.lower())
    try:
        while True:
            data:Config = await websocket.receive_json()
            await websocket_list.broadcast(data, user_name.lower())
    except WebSocketDisconnect:
        websocket_list.disconnect(websocket, user_name.lower())

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, host='0.0.0.0')