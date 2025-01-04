from fastapi import Request
from fastapi_users.authentication import AuthenticationBackend
from .transport import bearer_transport, cookie_transport
from .strategy import get_database_strategy, get_jwt_strategy

auth_db_backend = AuthenticationBackend(
    name="access_tokens_db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
auth_jwt_backend = AuthenticationBackend(
    name="bearer_jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

auth_cookie_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


async def get_enabled_backends(request: Request):
    """Return the enabled dependencies following custom logic."""
    if request.url.path == "/protected-route-only-jwt":
        return [auth_jwt_backend]
    else:
        return [auth_cookie_backend, auth_jwt_backend]
