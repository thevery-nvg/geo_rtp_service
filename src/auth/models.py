from fastapi_users_db_sqlalchemy import (SQLAlchemyBaseUserTable,
                                         SQLAlchemyUserDatabase)

from core.models.mixins.ID_intpk_mixin import IDIntPKMixin

from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey, Integer

from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IDIntPKMixin, SQLAlchemyBaseUserTable[int]):
    pass

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="cascade"),
        nullable=False
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, AccessToken)
