import os
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai
import logfire
import google.generativeai as genai2


from ..agent.helper.google_search import is_google_search

logfire.configure(environment=os.getenv("LOGFIRE_ENVIRONMENT"))

load_dotenv()


@dataclass
class BaseAgent:
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"), http_options={"api_version": "v1alpha"}
    )
    model_id = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}

    async def chat(self, message: str):
        async with self.client.aio.live.connect(
            model=self.model_id, config=self.config
        ) as session:
            logfire.info(str(message))
            # greetings_question = self.classify_question(message=message)
            greetings_question = True
            logfire.info(str(greetings_question))
            if greetings_question:
                message_after_processing = self.is_process_message(message=message)
                await session.send(input=message_after_processing, end_of_turn=True)
            # await session.send(input=message, end_of_turn=True)
            async for response in session.receive():
                if response.text is None:
                    continue
                yield {"type": "text", "content": response.text}

    def classify_question(self, message: str):
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
            model_name=self.model_id, generation_config={"temperature": 0}, tools=tools
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
        result_google = is_google_search(input=message, search_type="search")
        logfire.info(str(result_google))
        prompt = f"""
        Context:
        {result_google}
        Question:
        {message}
        Answer:
        """
        logfire.info(prompt)
        return prompt


base_agent = BaseAgent()
