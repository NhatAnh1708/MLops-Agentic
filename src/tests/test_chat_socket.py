import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

from ..agent.base_agent import base_agent
from ..agent.gemini_agent import gemini_agent

# Import các module cần thiết
from ..routes.chat_socket import websocket_router


@pytest.fixture
def test_client():
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(websocket_router)
    return TestClient(app)


@pytest.mark.asyncio
async def test_websocket_connection():
    with patch("fastapi.WebSocket") as MockWebSocket:
        mock_websocket = AsyncMock(spec=WebSocket)
        await websocket_text_endpoint(mock_websocket)
        mock_websocket.accept.assert_called_once()


@pytest.mark.asyncio
async def test_base_agent_chat():
    with patch("fastapi.WebSocket") as MockWebSocket:
        mock_websocket = AsyncMock(spec=WebSocket)

        # Mock receive_json để trả về message test
        mock_websocket.receive_json.return_value = {"text": "Hello", "agent": False}

        # Mock base_agent.chat
        mock_response = [{"content": "Test response"}]
        with patch.object(base_agent, "chat", return_value=mock_response):
            await websocket_text_endpoint(mock_websocket)

        # Verify các calls
        mock_websocket.accept.assert_called_once()
        mock_websocket.send_json.assert_any_call(
            {
                "text": "Test response",
                "gif_url": None,
                "type": "chunk",
                "format": "markdown",
            }
        )


@pytest.mark.asyncio
async def test_gemini_agent_chat():
    with patch("fastapi.WebSocket") as MockWebSocket:
        mock_websocket = AsyncMock(spec=WebSocket)

        # Mock receive_json để trả về message test với agent=True
        mock_websocket.receive_json.return_value = {"text": "Hello", "agent": True}

        # Mock gemini_agent.chat
        mock_response = [{"text": "Test response", "gif_url": "test.gif"}]
        with patch.object(gemini_agent, "chat", return_value=mock_response):
            await websocket_text_endpoint(mock_websocket)

        # Verify các calls
        mock_websocket.accept.assert_called_once()
        mock_websocket.send_json.assert_any_call(
            {
                "text": "Test response",
                "gif_url": "test.gif",
                "type": "chunk",
                "format": "markdown",
            }
        )


@pytest.mark.asyncio
async def test_error_handling():
    with patch("fastapi.WebSocket") as MockWebSocket:
        mock_websocket = AsyncMock(spec=WebSocket)

        # Mock receive_json để raise exception
        mock_websocket.receive_json.side_effect = Exception("Test error")

        await websocket_text_endpoint(mock_websocket)

        mock_websocket.send_json.assert_called_with(
            {"text": "Connection error. Please try again.", "type": "error"}
        )


@pytest.mark.asyncio
async def test_resource_exhausted_retry():
    with patch("fastapi.WebSocket") as MockWebSocket:
        mock_websocket = AsyncMock(spec=WebSocket)

        # Mock receive_json
        mock_websocket.receive_json.return_value = {"text": "Hello", "agent": True}

        # Mock gemini_agent.chat để raise RESOURCE_EXHAUSTED error
        with patch.object(
            gemini_agent, "chat", side_effect=Exception("RESOURCE_EXHAUSTED")
        ):
            await websocket_text_endpoint(mock_websocket)

        # Verify retry message
        mock_websocket.send_json.assert_any_call(
            {
                "text": f"API limit reached. Retrying in 2 seconds... (Attempt 1/3)",
                "type": "error",
            }
        )
