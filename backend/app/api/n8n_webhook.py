from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()


class WebhookRequest(BaseModel):
    data: Dict[str, Any]
    workflow: str = "default"


class WebhookResponse(BaseModel):
    success: bool
    message: str
    processed: bool


@router.post("/webhook", response_model=WebhookResponse)
async def n8n_webhook(request: WebhookRequest):
    """Webhook для интеграции с n8n"""
    try:
        # Обработка данных от n8n
        # Здесь можно добавить логику обработки
        
        return WebhookResponse(
            success=True,
            message="Webhook received",
            processed=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

