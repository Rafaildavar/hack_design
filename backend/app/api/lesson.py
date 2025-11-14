from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


class LessonRequest(BaseModel):
    topic: str
    level: str = "beginner"
    format: str = "summary"  # summary, plan, cards


class LessonResponse(BaseModel):
    content: str
    format: str


@router.post("/", response_model=LessonResponse)
async def generate_lesson(request: LessonRequest):
    """Генерация плана урока, конспекта или карточек"""
    try:
        format_prompts = {
            "summary": "Создай подробный конспект по теме",
            "plan": "Создай план урока по теме",
            "cards": "Создай карточки для запоминания по теме"
        }
        
        prompt = f"""{format_prompts.get(request.format, format_prompts['summary'])}: {request.topic}
        Уровень: {request.level}
        
        Структурируй информацию четко и понятно."""
        
        response = await ai_service.chat(prompt, "")
        return LessonResponse(
            content=response,
            format=request.format
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

