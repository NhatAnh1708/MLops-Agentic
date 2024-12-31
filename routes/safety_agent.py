from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..models.message import ChatMessageRequest, ChatMessageResponse

from ..agents.SafeComment.mask import SafeCommentAgent

router = APIRouter()

init_agent = {}

safe_comment_agent = SafeCommentAgent()

@router.post("/api/v1/safe-text", response_model=ChatMessageResponse, tags=["SafeAgent"])
async def generate_safe_text(request: ChatMessageRequest) -> ChatMessageResponse:
    """Generate safe text"""
    text_masked, is_toxic, is_safe = safe_comment_agent.masking_text(request.message)
    return ChatMessageResponse(message=text_masked, is_safe=is_safe, is_toxic=is_toxic)
