from fastapi import APIRouter
from app import routes
from app.routes import summary

api_router = APIRouter()
api_router.include_router(routes.router, prefix="/api/v1")
