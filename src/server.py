import os

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.routes.health import health_router
from src.routes.index import web_router
from src.routes.websocket import websocket_router

app = FastAPI()
logfire.configure(environment=os.getenv("LOGFIRE_ENVIRONMENT"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(websocket_router)
app.include_router(health_router)
app.include_router(web_router)
