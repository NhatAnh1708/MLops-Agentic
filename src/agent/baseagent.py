import os
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai
from loguru import logger

load_dotenv()


@dataclass
class BaseAgent:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"), http_options={"api_version": "v1alpha"}
    )
    model_id = "gemini-2.0-flash-exp"
    config = {"response_modalities": ["TEXT"]}

    async def chat(self, message):
        async with self.client.aio.live.connect(
            model=self.model_id, config=self.config
        ) as session:
            await session.send(input=message, end_of_turn=True)
            async for response in session.receive():
                if response.text is None:
                    continue
                yield {"type": "text", "content": response.text}


base_agent = BaseAgent()
