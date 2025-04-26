from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse
from passlib.context import CryptContext

from db.db_conn import SessionLocal
from db.models import User
from utils import helper

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        db: Session = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        if user and user.is_active and helper.verify_password(password, user.hashed_password):
            request.session.update({
                "user": user.email,
                "id": str(user.id)
            })
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user = request.session.get("user")
        id = request.session.get("id")

        if not user or not id:
            return False

        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == id).first()
        if not user or not user.is_active:
            return False
        return True
