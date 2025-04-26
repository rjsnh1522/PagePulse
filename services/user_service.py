from fastapi.params import Depends
from db.db_conn import get_db
from db.models import User


class UserService:

    @staticmethod
    def create_superuser(email, password, db: Depends(get_db)):
        existing_user = db.query(User).filter(User.email == email).first()
