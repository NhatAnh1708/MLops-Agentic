# Use repo : https://github.com/browser-use/web-ui

from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, SystemPrompt
from pydantic import SecretStr
import os
from dotenv import load_dotenv

load_dotenv()
api_key = 'AIzaSyDK0p6DWqlva2vKNgWuSAc2JJvJ6C-qdbs'

class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        # Get existing rules from parent class
        existing_rules = super().important_rules()

        # Add your custom rules
        new_rules = """
9. MOST IMPORTANT RULE:
- ALWAYS The language of the answer must be the same language as the input question.
""" 
        return f'{existing_rules}\n{new_rules}'

@dataclass
class GeminiAgent(MySystemPrompt):

    model = 'gemini-2.0-flash-exp'
    llm = ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
    
    async def chat(self, message: str):
        agent = Agent(
            task=message,
            llm=self.llm,
            system_prompt_class=MySystemPrompt
        )
        agent_history = await agent.run()
        result = agent_history.final_result()
        return result

gemini_agent = GeminiAgent()
