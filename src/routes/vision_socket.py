from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.agent.vision_agent import vision_agent

vision_router = APIRouter()


@vision_router.websocket("/ws/vision")
async def websocket_vision_endpoint(websocket: WebSocket):

    await websocket.accept()
    
    return {"status": "AI Assistant is running"}
