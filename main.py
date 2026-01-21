from fastapi import FastAPI
from app.core.config import settings
from app.core.config import settings
from app.api.router import router
from app.api.html_demo import html_router

app = FastAPI(title=settings.app_name)





app.include_router(router)
app.include_router(html_router)


@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running"}
