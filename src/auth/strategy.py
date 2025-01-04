from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from .dependencies.access_tokens import get_access_tokens_db
from core.config import settings
from fastapi_users.authentication import JWTStrategy

if TYPE_CHECKING:
    from .models import AccessToken


def get_database_strategy(
        access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_tokens_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(database=access_token_db,
                            lifetime_seconds=settings.access_token.lifetime_seconds)


SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
