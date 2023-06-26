from fastapi import APIRouter

from src.api.auth.views import router as auth_views

routes = APIRouter()

routes.include_router(
    auth_views,
    prefix="/auth",
)
