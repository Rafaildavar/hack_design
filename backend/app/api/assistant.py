from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


class AssistantRequest(BaseModel):
    message: str
    context: str = ""


class AssistantResponse(BaseModel):
    response: str
    context: str = ""


@router.post("/", response_model=AssistantResponse)
async def chat(request: AssistantRequest):
    """Диалог с AI-ассистентом"""
    try:
        response = await ai_service.chat(request.message, request.context)
        return AssistantResponse(
            response=response,
            context=request.context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

