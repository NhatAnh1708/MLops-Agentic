from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import base64
import logging
from io import BytesIO
from PIL import Image
from agent.vision_agent import vision_agent
import os
from datetime import datetime
from agent.vision_agent import cleanup_uploaded_images
vision_router = APIRouter()


@vision_router.websocket("/ws/vision")
async def websocket_vision_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # cleanup_uploaded_images()
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Extract text and frame
            text = data.get('text', '')
            frame_base64 = data.get('frame', '').split(',')[1]  # Remove data:image/jpeg;base64, prefix
            
            logging.info(f"Received text message: {text}")
            
            # Convert base64 frame to PIL Image
            frame_bytes = base64.b64decode(frame_base64)
            frame_image = Image.open(BytesIO(frame_bytes))
            
            # Lưu ảnh với tên file dựa trên timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_dir = "frontend/uploaded_images"
            os.makedirs(save_dir, exist_ok=True)
            image_path = os.path.join(save_dir, f"vision_{timestamp}.jpg")
            frame_image.save(image_path)
            
            response_text = await vision_agent.chat_with_image(frame_image, text)
            image_path = image_path.replace("frontend/", "static/")
            # Send response back to client with image path
            await websocket.send_json({
                "text": response_text,
                "image_path": image_path
            })
            
    except Exception as e:
        logging.error(f"Error in vision websocket: {str(e)}")
        # Try to send error message to client
        try:
            await websocket.send_json({
                "text": "Sorry, there was an error processing your request."
            })
        except:
            pass
    finally:
        # Clean up if needed
        logging.info("Vision WebSocket connection closed")
