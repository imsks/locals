from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes import api_router

load_dotenv()

app = FastAPI(
    title="Locals Agent",
    description="Local LLM agentic system with browser-use for web scraping",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")
