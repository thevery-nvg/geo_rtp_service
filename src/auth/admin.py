import hashlib
import secrets

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request


from auth.models import User
from core.config import settings


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        is_user_exist = username == settings.admin.username
        if is_user_exist:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
        else:
            return False
        if hashed_password == settings.admin.password:
            request.session.update(
                {
                    "token": settings.admin.token,
                }
            )
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(
    secret_key=settings.admin.secret
)
