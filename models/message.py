from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """Chat message request"""

    message: str = Field(..., title="Message", description="Message to send to chatbot")


class ChatMessageResponse(BaseModel):
    """Chat message response"""

    message: str = Field(..., title="Message", description="Message from chatbot")
    is_safe: bool = Field(..., title="Is Safe", description="Is safe message")
    is_toxic: bool = Field(..., title="Is Toxic", description="Is toxic message")
