import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

from agent.base_agent import base_agent
from agent.operator_agent import gemini_agent

load_dotenv()


websocket_router = APIRouter()

MAX_RETRIES = 3
RETRY_DELAY = 2


@websocket_router.websocket("/ws/text")
async def websocket_text_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            try:
                data = await websocket.receive_json()
                logger.info(str(data))

                if "text" in data:
                    retries = 0
                    while retries < MAX_RETRIES:
                        try:
                            # Sử dụng agent nếu flag được bật
                            if data["deepSearch"] and data["googleSearch"]:
                                async for response_chunk in gemini_agent.chat(
                                    message=data
                                ):
                                    await websocket.send_json(
                                        {
                                            "text": response_chunk["text"],
                                            "gif_url": response_chunk["gif_url"],
                                            "type": "chunk",
                                            "format": "markdown",
                                        }
                                    )
                            elif data["deepSearch"]:
                                async for response_chunk in gemini_agent.chat(
                                    message=data
                                ):
                                    await websocket.send_json(
                                        {
                                            "text": response_chunk["text"],
                                            "gif_url": response_chunk["gif_url"],
                                            "type": "chunk",
                                            "format": "markdown",
                                        }
                                    )
                            elif data["googleSearch"]:
                                async for response_chunk in base_agent.chat(
                                    message=data["text"], google_search=True
                                ):
                                    try:
                                        chunk_content = str(response_chunk["content"])
                                        await websocket.send_json(
                                            {
                                                "text": chunk_content,
                                                "gif_url": None,
                                                "type": "chunk",
                                                "format": "markdown",
                                            }
                                        )
                                    except Exception as send_error:
                                        logger.error(
                                            f"Error sending chunk: {send_error}"
                                        )
                                        await websocket.send_json(
                                            {
                                                "text": "Error sending response chunk",
                                                "type": "error",
                                            }
                                        )
                                        continue
                            else:
                                logger.info("Normal mode")
                                async for response_chunk in base_agent.chat(
                                    message=data["text"], google_search=False
                                ):
                                    try:
                                        chunk_content = str(response_chunk["content"])
                                        logger.info(f"Chunk content: {chunk_content}")
                                        await websocket.send_json(
                                            {
                                                "text": chunk_content,
                                                "gif_url": None,
                                                "type": "chunk",
                                                "format": "markdown",
                                            }
                                        )
                                    except Exception as send_error:
                                        logger.error(
                                            f"Error sending chunk: {send_error}"
                                        )
                                        await websocket.send_json(
                                            {
                                                "text": "Error sending response chunk",
                                                "type": "error",
                                            }
                                        )
                                        continue

                            await websocket.send_json({"type": "end"})
                            break
                        except Exception as process_error:
                            logger.error(f"Error processing message: {process_error}!")
                            error_message = str(process_error)
                            if "RESOURCE_EXHAUSTED" in error_message:
                                retries += 1
                                if retries < MAX_RETRIES:
                                    # Thông báo đang thử lại
                                    await websocket.send_json(
                                        {
                                            "text": f"API limit reached. Retrying in {RETRY_DELAY} seconds... (Attempt {retries}/{MAX_RETRIES})",
                                            "type": "error",
                                        }
                                    )
                                    await asyncio.sleep(RETRY_DELAY)
                                    continue
                                else:
                                    await websocket.send_json(
                                        {
                                            "text": "Sorry, the service is currently at capacity. Please try again later.",
                                            "type": "error",
                                        }
                                    )
                            else:
                                await websocket.send_json(
                                    {
                                        "text": "Sorry, there was an error processing your message. Please try again.",
                                        "type": "error",
                                    }
                                )
                            break

            except WebSocketDisconnect:
                logger.info("Client disconnected")
                break

            except Exception as e:
                logger.error(f"Connection error: {str(e)}!")
                try:
                    if websocket.client_state.CONNECTED:  # Kiểm tra trạng thái kết nối
                        await websocket.send_json(
                            {
                                "text": "Connection error. Please try again.",
                                "type": "error",
                            }
                        )
                except:
                    logger.error("Could not send error message to client")
                break  # Dừng tác vụ khi gặp lỗi
    finally:
        try:
            if websocket.client_state.CONNECTED:
                await websocket.close()
        except:
            pass
