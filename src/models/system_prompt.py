from browser_use import SystemPrompt


class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        existing_rules = super().important_rules()
        new_rules = """
9. MOST IMPORTANT RULE:
- ALWAYS The language of the answer must be the same language as the input question.

If Google is asking to verify I am not a robot.
Please click on the checkbox and then click on the "Verify" button or click I'm not a robot.
If it asks for more verification, please follow the instructions
"""
        return f"{existing_rules}\n{new_rules}"
