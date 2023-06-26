from fastapi import APIRouter

from src.schemas.auth import EmployeeCreate, EmployeeRead

from .settings import auth_backend, fastapi_users

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(EmployeeRead, EmployeeCreate),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(EmployeeRead),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/jwt",
    tags=["auth"],
)
