from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import assistant, schedule, lesson, image, telegram, n8n_webhook

app = FastAPI(
    title="hac_ API",
    description="AI-powered educational assistant API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["schedule"])
app.include_router(lesson.router, prefix="/api/lesson", tags=["lesson"])
app.include_router(image.router, prefix="/api/image", tags=["image"])
app.include_router(telegram.router, prefix="/api/tg", tags=["telegram"])
app.include_router(n8n_webhook.router, prefix="/api/n8n", tags=["n8n"])


@app.get("/")
async def root():
    return {"message": "hac_ API is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

