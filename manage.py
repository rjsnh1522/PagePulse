# fmt: off
from dotenv import load_dotenv

from utils import helper

load_dotenv('.env')
# fmt: on

import typer
from getpass import getpass
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.db_conn import get_db
from db.models import User

app = typer.Typer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.command(name="create super user")
def create_superuser():
    """Create a new superuser."""
    email = typer.prompt("Enter email")
    password = getpass("Enter password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        typer.echo("❌ Passwords do not match.")
        raise typer.Exit()

    db: Session = next(get_db())
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        typer.echo("❌ A user with this email already exists.")
        raise typer.Exit()

    hashed_password = helper.get_password_hash(password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    typer.echo("✅ Superuser created successfully.")




if __name__ == "__main__":
    app()