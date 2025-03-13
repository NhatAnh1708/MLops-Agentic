import os
from dataclasses import dataclass

import google.generativeai as genai2
from dotenv import load_dotenv
from google import genai
import asyncio
from loguru import logger
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

from agent.helper.google_search import is_google_search

load_dotenv()


@dataclass
class BaseAgent:
    """
    Base agent for the Gemini model.
    """

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"), http_options={"api_version": "v1alpha"}
    )
    model_name = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}
    llm_qwen = ChatOllama(
        model="qwen2.5",
        num_ctx=32000,
        base_url="https://6a4f-34-125-97-236.ngrok-free.app"
    )
    async def chat_qwen(self, message: str, google_search: bool = False):
        """
        Chat with the Qwen model.
        """
        try:
            if google_search:
                message_after_processing = self.is_process_message(message=message)
            else:
                message_after_processing = message
            message_ollama = [
                ("human", message_after_processing)
            ]
            response = self.llm_qwen.stream(message_ollama)
            for chunk in response:
                if chunk.content is None:
                    continue
                yield {"type": "text", "content": chunk.content}
                await asyncio.sleep(0.001)
        except Exception as e:
            logger.error(f"Error in chat_qwen: {e}")


    async def chat(self, message: str):
        """
        Chat with the Gemini model.
        """
        async with self.client.aio.live.connect(
            model=self.model_name, config=self.config
        ) as session:
            logger.info(str(message))
            # greetings_question = self.classify_question(message=message)
            greetings_question = True
            if greetings_question:
                message_after_processing = self.is_process_message(message=message)
                await session.send(input=message_after_processing, end_of_turn=True)
            async for response in session.receive():
                if response.text is None:
                    continue
                yield {"type": "text", "content": response.text}

    def classify_question(self, message: str):
        """
        Classify the question.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai2.configure(api_key=api_key)
        # Define function schema
        tools = [
            {
                "function_declarations": [
                    {
                        "name": "is_greetings_question",
                        "description": "Determines if the given message is a greeting question",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "The message to check",
                                }
                            },
                            "required": ["message"],
                        },
                    }
                ]
            }
        ]

        model = genai2.GenerativeModel(
            model_name=self.model_name, generation_config={"temperature": 0}, tools=tools
        )

        chat = model.start_chat()
        response = chat.send_message(
            f"""Determine if this message is a greeting question: "{message}"
        Only respond with a function call to is_greetings_question.
        A greeting includes hello, hi, hey, good morning/afternoon/evening, etc....""",
            tools=tools,
        )

        # Check if function was called and return result
        if response.candidates[0].content.parts[0].function_call:
            return True
        return False

    def is_process_message(self, message: str):
        """
        Process the message.
        """
        result_google = is_google_search(input=message, search_type="search")
        prompt = f"""
        Context:
        {result_google}
        Question:
        {message}
        Answer:
        """
        return prompt


base_agent = BaseAgent()
