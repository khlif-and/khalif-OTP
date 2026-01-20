from fastapi import FastAPI
from app.core.config import settings
from app.api.router import router

app = FastAPI(title=settings.app_name)

@app.on_event("startup")
async def startup_event():
    from app.services.telegram_service import TelegramService
    import asyncio
    asyncio.create_task(TelegramService.start_polling())

app.include_router(router)

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running"}
