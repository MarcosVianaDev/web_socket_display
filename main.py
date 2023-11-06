from typing import Annotated
from fastapi import FastAPI, WebSocket, Path, Query, Body, status #Path e Query ajudam a documentação e validação automática
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from templatesRender import Render


class User(BaseModel):
    user_name: str
    user_pass: str

class Config(BaseModel):
    user_pass: str = ''
    texto: str = 'Exemplo'
    cor_fonte: str = '#0000ff'
    cor_fundo: str = '#cccccc'
    anim: str = 'slide'
    tempo_segundos: str = '10'
    
users = {}

config_default = Config().model_dump()


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=Render('index.html'), status_code=200)

@app.post('/criar')
def criar(user: User):
    new_config = Config()
    new_config.user_pass = user.user_pass
    users[user.user_name] = new_config.model_dump()
    print(users)
    return JSONResponse(content=f'user {user.user_name} created', status_code=status.HTTP_201_CREATED)


@app.get('/logar/{user_name}/edit')
def edit(user_name: str):
    return HTMLResponse(content=Render('criar.html', {'user_name':user_name}), status_code=200)

@app.get('/logar/{user_name}')
def logar(user_name: str):
    return HTMLResponse(content=Render('logar.html', {'user_name':user_name, 'tempo_segundos': config_default.get('tempo_segundos')}), status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # print(config_default)
    print(id(websocket))
    await websocket.send_json(config_default)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)