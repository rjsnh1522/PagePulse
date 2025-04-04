
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.util import hybridproperty

from sqlalchemy.dialects.postgresql import UUID

from utils import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)  # Store encrypted password
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())



class Website(Base):
    __tablename__ = "websites"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    domain = Column(String, unique=True, index=True)  # Unique domain name
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # link to user model
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    unique_id = Column(String, index=True, unique=True)  # Stored in LocalStorage
    ip = Column(String, index=True)  # Store actual IP
    ipv6 = Column(String, index=True)  # Store actual IPv6
    user_agent = Column(String)
    browser = Column(String)
    device = Column(String)
    platform = Column(String)
    country = Column(String)
    first_visit = Column(DateTime(timezone=True), server_default=func.now())
    last_visit = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID primary key
    website_id = Column(UUID(as_uuid=True), ForeignKey("websites.id"))  # Link to website
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id"))  # Link to visitor
    page_url = Column(String)  # Full URL of the page
    referrer = Column(String, nullable=True)  # Where they came from
    landing_page = Column(String)  # First page visited in the session
    session_duration = Column(Float, default=0.0)  # Time spent on page (seconds)
    scroll_depth = Column(Float, default=0.0)  # Scroll % (0-100)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())  # UTC timestamp