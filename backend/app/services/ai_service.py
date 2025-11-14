import os
from openai import AsyncOpenAI
import httpx

class AIService:
    def __init__(self):
        self.openai_client = None
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = AsyncOpenAI(api_key=openai_key)
        
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
    
    async def chat(self, message: str, context: str = "") -> str:
        """Отправка запроса к AI модели"""
        # Приоритет: OpenAI, затем Mistral
        if self.openai_client:
            return await self._chat_openai(message, context)
        elif self.mistral_key:
            return await self._chat_mistral(message, context)
        else:
            # Fallback - возвращаем заглушку для демо
            return f"AI Response to: {message}\n\n[AI service not configured. Please set OPENAI_API_KEY or MISTRAL_API_KEY]"
    
    async def _chat_openai(self, message: str, context: str) -> str:
        """Использование OpenAI"""
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": message})
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI: {str(e)}"
    
    async def _chat_mistral(self, message: str, context: str) -> str:
        """Использование Mistral"""
        try:
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.mistral_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "mistral-tiny",
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error with Mistral: {str(e)}"

