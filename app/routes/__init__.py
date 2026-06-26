from fastapi import APIRouter

from app.routes.health import router as health_router
from app.routes.myneta import router as myneta_router
from app.routes.scrape import router as scrape_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(scrape_router, prefix="/scrape", tags=["scrape"])
api_router.include_router(myneta_router, prefix="/scrape", tags=["scrape"])
