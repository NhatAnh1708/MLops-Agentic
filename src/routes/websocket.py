import os

import asyncio

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logfire


from src.agent.baseagent import base_agent

load_dotenv()
logfire.configure(environment=os.getenv("LOGFIRE_ENVIRONMENT"))

websocket_router = APIRouter()

MAX_RETRIES = 3
RETRY_DELAY = 2


@websocket_router.websocket("/ws/text")
async def websocket_text_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            logfire.info(str(data))
            if "text" in data:
                retries = 0
                while retries < MAX_RETRIES:
                    try:
                        current_response = ""
                        async for response_chunk in base_agent.chat(
                            message=data["text"]
                        ):
                            logfire.info(f"Response chunk content: {response_chunk}")
                            try:
                                chunk_content = str(response_chunk["content"])
                                current_response += chunk_content

                                await websocket.send_json(
                                    {
                                        "text": current_response,
                                        "type": "chunk",
                                        "format": "markdown",
                                    }
                                )
                            except Exception as send_error:
                                logfire.error(f"Error sending chunk: {send_error}")
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
                        logfire.error("Error processing message: %s!", process_error)
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
            logfire.info("Client disconnected")
            break

        except Exception as e:
            logfire.error("Connection error: %s!", e)
            try:
                await websocket.send_json(
                    {"text": "Connection error. Please try again.", "type": "error"}
                )
            except:
                logfire.error("Could not send error message to client")
            continue
