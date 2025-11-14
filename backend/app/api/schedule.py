from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


class ScheduleRequest(BaseModel):
    subjects: List[str]
    hours_per_week: int
    preferences: Optional[str] = ""


class ScheduleResponse(BaseModel):
    schedule: dict
    message: str


@router.post("/", response_model=ScheduleResponse)
async def generate_schedule(request: ScheduleRequest):
    """Генерация расписания"""
    try:
        prompt = f"""Создай расписание занятий для следующих предметов: {', '.join(request.subjects)}.
        Всего часов в неделю: {request.hours_per_week}
        Предпочтения: {request.preferences or 'нет'}
        
        Верни расписание в формате JSON с днями недели и временем занятий."""
        
        response = await ai_service.chat(prompt, "")
        return ScheduleResponse(
            schedule={"generated": True, "data": response},
            message="Расписание успешно сгенерировано"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

