import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes.chat_socket import websocket_router
from routes.health import health_router
from routes.index import web_router
from routes.voice_socket import voice_routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RUNNING_IN_DOCKER = os.path.exists("/.dockerenv")
if RUNNING_IN_DOCKER:
    BASE_DIR = "/app"
else:
    BASE_DIR = os.path.abspath("./")

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.include_router(websocket_router)
app.include_router(health_router)
app.include_router(web_router)
app.include_router(voice_routers)
