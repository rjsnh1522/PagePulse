from fastapi import APIRouter
from api import analytics

api_router = APIRouter()

api_router.include_router(analytics.router)