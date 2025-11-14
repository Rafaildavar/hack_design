from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os

router = APIRouter()


class TelegramRequest(BaseModel):
    message: str
    chat_id: str = None


class TelegramResponse(BaseModel):
    success: bool
    message: str


@router.post("/send", response_model=TelegramResponse)
async def send_telegram(request: TelegramRequest):
    """Отправка сообщения в Telegram через бота"""
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = request.chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            raise HTTPException(status_code=500, detail="Telegram credentials not configured")
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": request.message,
            "parse_mode": "HTML"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        
        return TelegramResponse(
            success=True,
            message="Сообщение отправлено"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

