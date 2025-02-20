from fastapi import APIRouter, WebSocket
from dataclasses import dataclass
from typing import Dict, Any
import asyncio
import json
import os
from google import genai
import base64
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
)

# from llama_index.embeddings.gemini import GeminiEmbedding
# from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


voice_routers = APIRouter()


@dataclass
class GeminiConfig:
    """Configuration for Gemini API connection"""

    api_key: str = os.environ["GOOGLE_API_KEY"]
    model: str = "gemini-2.0-flash-exp"
    embedding_model: str = "models/text-embedding-004"
    system_instruction: str = """You are a helpful assistant and you MUST always use the query_docs tool to query the document 
    towards any questions. It is mandatory to base your answers on the information from the output of the query_docs tool, 
    and include the context from the query tool in your response to the user's question.
    Do not mention your operations like "I am searching the document now".
    """


class DocumentIndex:
    """Handles document indexing and querying operations"""

    def __init__(
        self, storage_dir: str = "./storage", download_dir: str = "./downloads"
    ):
        self.storage_dir = storage_dir
        self.download_dir = download_dir
        self.llm = Gemini(
            api_key=GeminiConfig.api_key, model_name="models/gemini-2.0-flash-exp"
        )
        self.embedding_model = GeminiEmbedding(
            api_key=GeminiConfig.api_key, model_name="models/text-embedding-004"
        )
        Settings.llm = self.llm
        Settings.embed_model = self.embedding_model

    def build_index(self) -> VectorStoreIndex:
        """Build or load the document index"""
        if not os.path.exists(self.storage_dir):
            documents = SimpleDirectoryReader(self.download_dir).load_data()
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir=self.storage_dir)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
            index = load_index_from_storage(storage_context)
        return index

    def query_docs(self, query: str) -> str:
        """Query the document index"""
        index = self.build_index()
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        response_text = str(response)
        logger.info(f"RAG response: {response_text}")
        return response_text


class GeminiSession:
    """Manages the Gemini API session and websocket communication"""

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        # self.doc_index = doc_index
        self.client = genai.Client(http_options={"api_version": "v1alpha"})
        self.session = None

    async def handle_pdf_upload(self, chunk: Dict[str, Any]) -> None:
        """Handle PDF file upload and indexing"""
        pdf_data = base64.b64decode(chunk["data"])
        filename = chunk.get("filename", "uploaded.pdf")

        os.makedirs("./downloads", exist_ok=True)
        file_path = os.path.join("./downloads", filename)

        with open(file_path, "wb") as f:
            f.write(pdf_data)

        logger.info(f"Saved PDF file to {file_path}")

        if os.path.exists("./storage"):
            import shutil

            shutil.rmtree("./storage")

        self.doc_index.build_index()

        await self.websocket.send_json(
            {"text": f"PDF file {filename} has been uploaded and indexed successfully."}
        )

    async def handle_tool_call(self, response) -> None:
        """Handle tool calls from Gemini"""
        function_calls = response.tool_call.function_calls
        function_responses = []

        for function_call in function_calls:
            if function_call.name == "query_docs":
                try:
                    result = self.doc_index.query_docs(function_call.args["query"])
                    function_responses.append(
                        {
                            "name": function_call.name,
                            "response": {"result": result},
                            "id": function_call.id,
                        }
                    )
                    await self.websocket.send_json(
                        {"text": json.dumps(function_responses)}
                    )
                except Exception as e:
                    logger.info(f"Error executing function: {e}")
                    continue

        await self.session.send(input=function_responses)

    async def send_to_gemini(self) -> None:
        """Send messages from websocket to Gemini"""
        try:
            while True:
                message = await self.websocket.receive_text()
                try:
                    data = json.loads(message)
                    if "realtime_input" in data:
                        for chunk in data["realtime_input"]["media_chunks"]:
                            if chunk["mime_type"] == "audio/pcm":
                                await self.session.send(
                                    input={
                                        "mime_type": "audio/pcm",
                                        "data": chunk["data"],
                                    }
                                )
                            elif chunk["mime_type"] == "application/pdf":
                                await self.handle_pdf_upload(chunk)
                except Exception as e:
                    logger.info(f"Error sending to Gemini: {e}")
        except Exception as e:
            logger.info(f"WebSocket disconnected: {e}")
        finally:
            logger.info("send_to_gemini closed")

    async def receive_from_gemini(self) -> None:
        """Receive and process responses from Gemini"""
        try:
            while True:
                try:
                    async for response in self.session.receive():
                        if response.server_content is None:
                            if response.tool_call is not None:
                                await self.handle_tool_call(response)
                                continue

                        model_turn = response.server_content.model_turn
                        if model_turn:
                            await self.process_model_turn(model_turn)

                        if response.server_content.turn_complete:
                            logger.info("\n<Turn complete>")
                except Exception as e:
                    logger.info(f"Error receiving from Gemini: {e}")
                    break
        finally:
            logger.info("Gemini connection closed (receive)")

    async def process_model_turn(self, model_turn) -> None:
        """Process model turn responses"""
        for part in model_turn.parts:
            if hasattr(part, "text") and part.text is not None:
                await self.websocket.send_json({"text": part.text})
            elif hasattr(part, "inline_data") and part.inline_data is not None:
                base64_audio = base64.b64encode(part.inline_data.data).decode("utf-8")
                await self.websocket.send_json({"audio": base64_audio})
                logger.info("audio received")

    async def start(self) -> None:
        """Start the Gemini session"""
        try:
            config_message = await self.websocket.receive_text()
            config_data = json.loads(config_message)
            config = config_data.get("setup", {})
            config["system_instruction"] = GeminiConfig.system_instruction
            config["tools"] = [tool_query_docs]

            async with self.client.aio.live.connect(
                model=GeminiConfig.model, config=config
            ) as session:
                self.session = session
                logger.info("Connected to Gemini API")

                send_task = asyncio.create_task(self.send_to_gemini())
                receive_task = asyncio.create_task(self.receive_from_gemini())
                await asyncio.gather(send_task, receive_task)
        except Exception as e:
            logger.info(f"Error in Gemini session: {e}")
        finally:
            logger.info("Gemini session closed.")


# Define the tool (function)
tool_query_docs = {
    "function_declarations": [
        {
            "name": "query_docs",
            "description": "Query the document content with a specific query string.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "The query string to search the document index.",
                    }
                },
                "required": ["query"],
            },
        }
    ]
}


@voice_routers.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # doc_index = DocumentIndex()
    session = GeminiSession(websocket)
    try:
        await session.start()
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
