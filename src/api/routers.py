from fastapi import APIRouter

from src.api.auth.views import router as auth_views
from src.api.employee.views import router as employee_info_views


routes = APIRouter()

routes.include_router(
    auth_views,
    prefix="/auth",
)

routes.include_router(employee_info_views, prefix="/employee")
