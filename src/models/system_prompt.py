from browser_use import SystemPrompt


class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        existing_rules = super().important_rules()
        new_rules = """
9. MOST IMPORTANT RULE:
- ALWAYS The language of the answer must be the same language as the input question.
"""
        return f"{existing_rules}\n{new_rules}"
