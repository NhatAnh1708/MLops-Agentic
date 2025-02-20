import os
from dataclasses import dataclass

from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from models.google_search import ShoppingSearchResult
from agent.helper.google_search import is_google_search


@dataclass
class AiAgent:
    model = GroqModel(
        "llama-3.3-70b-versatile",
        api_key="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",
    )

    def chat(
        self, message: str, system_prompt: str = "Be concise, reply with one sentence."
    ):
        # data_google = is_google_search(input=message, search_type='search')
        # print(data_google)
        agent = Agent(
            self.model,
            system_prompt=system_prompt,
        )
        result = agent.run_sync(message)
        return result.data


ai_agent = AiAgent()
