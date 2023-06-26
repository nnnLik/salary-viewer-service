import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    JWTStrategy,
    BearerTransport,
    AuthenticationBackend,
)

from src.api.auth.manager import get_user_manager
from src.models.employee import Employee

from config.settings import settings

SECRET: str = settings.server.SECRET
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[Employee, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
