from typing import TYPE_CHECKING

from fastapi import Depends

from core.models import db_helper
from auth.models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
        session: "AsyncSession" = Depends(db_helper.session_getter)):
    yield AccessToken.get_db(session=session)
