import os
import httpx

class ImageService:
    def __init__(self):
        self.flux_key = os.getenv("FLUX_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
    
    async def generate(self, prompt: str) -> str:
        """Генерация изображения"""
        # Приоритет: Flux, затем OpenAI DALL-E
        if self.flux_key:
            return await self._generate_flux(prompt)
        elif self.openai_key:
            return await self._generate_openai(prompt)
        else:
            # Fallback - возвращаем placeholder
            return "https://via.placeholder.com/512x512?text=Image+Generation+Not+Configured"
    
    async def _generate_flux(self, prompt: str) -> str:
        """Использование Flux для генерации изображений"""
        try:
            # Пример интеграции с Flux API
            # Замените на реальный API endpoint
            url = "https://api.flux.ai/v1/generate"
            headers = {
                "Authorization": f"Bearer {self.flux_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "width": 512,
                "height": 512
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data.get("image_url", "https://via.placeholder.com/512x512")
        except Exception as e:
            # Fallback на placeholder
            return f"https://via.placeholder.com/512x512?text=Flux+Error"
    
    async def _generate_openai(self, prompt: str) -> str:
        """Использование OpenAI DALL-E"""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_key)
            
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="512x512",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            return f"https://via.placeholder.com/512x512?text=DALL-E+Error"

