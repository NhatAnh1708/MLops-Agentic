import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

load_dotenv()
web_router = APIRouter()

RUNNING_IN_DOCKER = os.path.exists("/.dockerenv")

if RUNNING_IN_DOCKER:
    BASE_DIR = "/app"
else:
    BASE_DIR = os.path.abspath("./")

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if not os.path.exists(FRONTEND_DIR):
    raise Exception(f"Error: FRONTEND_DIR '{FRONTEND_DIR}' not found.")

templates = Jinja2Templates(directory=FRONTEND_DIR)

text_ws_url = os.getenv("VITE_TEXT_WS_URL")
voice_ws_url = os.getenv("VITE_VOICE_WS_URL")


@web_router.get("/")
async def get(request: Request):
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "TEXT_WS_URL": text_ws_url,
                "VOICE_WS_URL": voice_ws_url,
            },
        )
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: index.html not found</h1>", status_code=404
        )
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error loading page: {str(e)}</h1>", status_code=500
        )
