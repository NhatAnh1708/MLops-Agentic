# Use repo : https://github.com/browser-use/web-ui

import asyncio
import os
from dataclasses import dataclass
from typing import AsyncGenerator

from browser_use import Agent, Browser, BrowserConfig
from browser_use.agent.views import AgentOutput
from browser_use.browser.views import BrowserState
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from lmnr import Laminar as lr
from loguru import logger
from pydantic import SecretStr

from agent.helper.screenshot import base64_to_image, cleanup_screenshots
from models.system_prompt import MySystemPrompt

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
lr.initialize(project_api_key=os.getenv("LAMINAR_API_KEY"))

@dataclass
class GeminiAgent(MySystemPrompt):
    """
    Operator agent using Gemini model.
    """

    model = "gemini-2.0-flash-exp"
    llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
    browser = Browser(config=BrowserConfig(
        headless=False, 
        disable_security=False
    ))
    # TODO: Use remote browser with noVNC
    # browser = Browser(
    # config = BrowserConfig(
    #     cdp_url="ws://192.168.215.3:4444/devtools/browser/5b8e295a-3153-4dc5-871c-4bd2f4337068"
    # ))
    data_queue = asyncio.Queue()
    screenshot_path = "frontend/screenshots"

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
        # Create the agent task
        agent_task = asyncio.create_task(agent.run(max_steps=10))
        logger.info(f"Agent task: {agent_task}")
        try:
            while not agent_task.done():
                try:
                    step_data = await asyncio.wait_for(
                        self.data_queue.get(), timeout=60
                    )
                    logger.info(f"Step data: {step_data}")
                    valid_data = {
                        "step": step_data.get("step", 0),
                        "screenshot_path": step_data.get("screenshot_path", ""),
                        "thoughts": step_data.get("thoughts", {}),
                        "actions": step_data.get("actions", []),
                        "url": step_data.get("url", ""),
                        "title": step_data.get("title", ""),
                    }
                    output_after_processing = self.process_output(valid_data)

                    # TODO: Remove this condition
                    if valid_data["step"] != 2:
                        image_step = valid_data["screenshot_path"].replace(
                            "frontend/", "static/"
                        )
                        data = {"text": output_after_processing, "gif_url": image_step}
                    else:
                        data = {"text": output_after_processing, "gif_url": None}
                    yield data

                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for agent data")
                    break

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise
        finally:
            if not agent_task.done():
                agent_task.cancel()
                try:
                    await agent_task
                except asyncio.CancelledError:
                    pass

    def process_output(self, valid_data: dict):
        """
        Process the output of the agent.
        """
        if "done" in valid_data["actions"][0]:
            return valid_data["actions"][0]["done"]["text"]
        output = (
            f"\n"
            f"### 📍 Step: {valid_data['step']}\n"
            f"🧠 **Memory:** {valid_data['thoughts']['memory']}\n"
            f"🎯 **Next Goal:** {valid_data['thoughts']['next_goal']}\n"
            f"🛠️ **Actions:**"
            f"{', '.join([str(action) for action in valid_data['actions']])}\n"
            f"🔗 **Link:** <a href='{valid_data['url']}'>{valid_data['url']}</a>\n"
            f"🔍 **Title:** {valid_data['title']}\n"
        )
        return output

    async def new_step_callback(
        self, state: BrowserState, model_output: AgentOutput, steps: int
    ):
        """Callback để gửi dữ liệu vào queue"""
        path = f"{self.screenshot_path}/{steps}.png"
        last_screenshot = state.screenshot
        img_path = base64_to_image(
            base64_string=str(last_screenshot), output_filename=path
        )
        thoughts = {
            "evaluation": model_output.current_state.evaluation_previous_goal,
            "memory": model_output.current_state.memory,
            "next_goal": model_output.current_state.next_goal,
        }
        actions = [
            action.model_dump(exclude_unset=True) for action in model_output.action
        ]

        step_data = {
            "step": steps,
            "screenshot_path": img_path,
            "thoughts": thoughts,
            "actions": actions,
            "url": state.url,
            "title": state.title,
        }
        await self.data_queue.put(step_data)


gemini_agent = GeminiAgent()
