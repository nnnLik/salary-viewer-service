from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)


from config.settings import Settings

cookie_transport: CookieTransport = CookieTransport(cookie_max_age=3600)

SECRET: str = Settings.server.SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
