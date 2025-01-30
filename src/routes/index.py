import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

web_router = APIRouter()


@web_router.get("/")
async def get():
    # Đọc file index.html từ thư mục notebooks/poc
    html_path = os.path.join("frontend", "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page: {str(e)}</h1>")
