from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.agent.base_agent import BaseAgent
from PIL import Image
from loguru import logger
load_dotenv()



@dataclass
class VisionAgent(BaseAgent):


    async def image_capture(self):
        """
        Capture image from the screen.
        """
        pass
    
    async def chat_with_image(self, img: Image, prompt: str):
        response = self.clientmodels.generate_content(
            model=self.model_name,
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                system_instruction="Answer the question based on the image",
                temperature=0.01,
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_ONLY_HIGH",
                    ),
                ],
            ),
        )
        logger.info("Response:")
        logger.info(str(response.text))
        return response.text


vision_agent = VisionAgent()