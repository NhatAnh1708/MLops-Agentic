from dataclasses import dataclass



@dataclass
class BaseAgent:
    """Base class for all agents"""
    model_name: str
    


    def generate_text(self, text: str) -> str:
        """Generate text"""
        return text
    