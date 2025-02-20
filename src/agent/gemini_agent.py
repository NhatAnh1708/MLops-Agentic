# Use repo : https://github.com/browser-use/web-ui

from dataclasses import dataclass
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, SystemPrompt, Browser, BrowserConfig
from browser_use.browser.views import BrowserState
from browser_use.agent.views import AgentOutput
from pydantic import SecretStr
import os
from dotenv import load_dotenv
from lmnr import Laminar as lr
from src.agent.helper.screenshot import cleanup_screenshots, base64_to_image
from loguru import logger
from redis import Redis
import json
from typing import AsyncGenerator
from queue import Queue
import asyncio

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
redis_client = Redis(host="localhost", port=6379, db=0)

lr.initialize(project_api_key=os.getenv("LAMINAR_API_KEY"))


# exporter = OTLPSpanExporter(
#     endpoint="https://0.0.0.0:8001/v1/traces",
#     # important: `authorization` starts with a lowercase letter
#     headers={"authorization": f"Bearer {os.getenv('LAMINAR_API_KEY')}"},
# )

# lr.function_that_initiates_tracer(
#     exporter=exporter,
#     # other parameters
# )


class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
9. MOST IMPORTANT RULE:
- ALWAYS The language of the answer must be the same language as the input question.
"""
        return f"{existing_rules}\n{new_rules}"

@dataclass
class GeminiAgent(MySystemPrompt):
    model = "gemini-2.0-flash-exp"
    llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
    browser = Browser(config=BrowserConfig(headless=True))
    data_queue = asyncio.Queue()  # Dùng async queue

    async def chat(self, message: str) -> AsyncGenerator[dict, None]:
        """Streaming dữ liệu theo kiểu yield"""
        cleanup_screenshots()
        agent = Agent(
            task=message,
            llm=self.llm,
            browser=self.browser,
            system_prompt_class=MySystemPrompt,
            register_new_step_callback=self.new_step_callback,
        )
        agent_task = asyncio.create_task(agent.run(max_steps=10))
        logger.info(f"Agent task: {agent_task}")
        while True:
            step_data = await asyncio.wait_for(self.data_queue.get(), timeout=60)
            valid_data = {
                "step": step_data['step'],
                "screenshot_path": step_data['screenshot_path'],
                "thoughts": step_data['thoughts'],
                "actions": step_data['actions'],
                "url": step_data['url'],
                "title": step_data['title'],
            }
            output_after_processing = self.process_output(valid_data)
            if valid_data['step'] != 2:
                image_step = valid_data['screenshot_path'].replace("frontend/", "static/")
                data = {"text": output_after_processing, "gif_url": image_step}
            else:
                data = {"text": output_after_processing, "gif_url": None}  # Không có gif_url cho step 2
            
            yield data

    def process_output(self, valid_data: dict):        
        if 'done' in valid_data['actions'][0]:
            return valid_data['actions'][0]['done']['text']
        output = (
            f"\n"
            f"### 📍 Step: {valid_data['step']}\n"
            f"🧠 **Memory:** {valid_data['thoughts']['memory']}\n"
            f"🎯 **Next Goal:** {valid_data['thoughts']['next_goal']}\n"
            f"🛠️ **Actions:**\n"
            f"- {', '.join([str(action) for action in valid_data['actions']])}\n"
            f"🔗 **URL:** {valid_data['url']}\n"
            f"🔍 **Title:** {valid_data['title']}\n"
        )
        return output

    def new_step_callback(self, state: BrowserState, model_output: AgentOutput, steps: int):
        """Callback để gửi dữ liệu vào queue"""
        path = f"frontend/screenshots/{steps}.png"
        last_screenshot = state.screenshot
        img_path = base64_to_image(base64_string=str(last_screenshot), output_filename=path)

        thoughts = {
            "page_summary": model_output.current_state.page_summary,
            "evaluation": model_output.current_state.evaluation_previous_goal,
            "memory": model_output.current_state.memory,
            "next_goal": model_output.current_state.next_goal,
        }
        actions = [action.model_dump(exclude_unset=True) for action in model_output.action]

        step_data = {
            "step": steps,
            "screenshot_path": img_path,
            "thoughts": thoughts,
            "actions": actions,
            "url": state.url,
            "title": state.title,
        }
        asyncio.create_task(self.data_queue.put(step_data))  # Đẩy vào queue async
        logger.info(f"Data added to queue: {step_data}")


gemini_agent = GeminiAgent()
