from db.models import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models so that Alembic sees them
