from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()


class ImageRequest(BaseModel):
    prompt: str
    style: str = "educational"  # educational, meme, diagram


class ImageResponse(BaseModel):
    image_url: str
    prompt: str


@router.post("/", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    """Генерация изображений (учебные иллюстрации / мемы / схемы)"""
    try:
        style_prompts = {
            "educational": f"Educational illustration: {request.prompt}, clean, professional, academic style",
            "meme": f"Funny educational meme: {request.prompt}, humorous, engaging",
            "diagram": f"Educational diagram: {request.prompt}, clear, schematic, informative"
        }
        
        final_prompt = style_prompts.get(request.style, style_prompts["educational"])
        image_url = await image_service.generate(final_prompt)
        
        return ImageResponse(
            image_url=image_url,
            prompt=request.prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

