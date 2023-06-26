import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)

from src.api.auth.manager import get_user_manager
from src.models.employee import Employee

from config.settings import settings

cookie_transport: CookieTransport = CookieTransport(cookie_max_age=3600)
SECRET: str = settings.server.SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[Employee, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
