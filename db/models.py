
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

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,  default=uuid.uuid4)
    unique_id = Column(String, index=True, unique=True)  # Stored in LocalStorage
    first_visit = Column(DateTime(timezone=True), server_default=func.now())
    last_visit = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID primary key
    website_id = Column(UUID(as_uuid=True), ForeignKey("websites.id"))  # Link to website
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id"))  # Link to visitor

    visitor_session_id = Column(String) # visitor_session_id
    page_url = Column(String)  # Full URL of the page
    current_page_path = Column(String)
    domain_name = Column(String)
    referrer = Column(String, nullable=True)  # Where they came from
    landing_page = Column(String)  # First page visited in the session
    session_duration = Column(Float, default=0.0)  # Time spent on page (seconds)
    scroll_depth = Column(Float, default=0.0)  # Scroll % (0-100)
    ip = Column(String, index=True)  # Store actual IP
    ipv6 = Column(String, index=True)  # Store actual IPv6
    user_agent = Column(String)
    browser = Column(String)
    browser_secondary = Column(String)
    device = Column(String)
    page_height = Column(Float, default=0.0)
    platform = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())  # UTC timestamp

    user_location = relationship("UserLocation", backref="analytics", uselist=False)



class UserLocation(Base):
    __tablename__ = "user_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    analytics_id = Column(UUID(as_uuid=True), ForeignKey("analytics.id"), nullable=False)

    ip = Column(String, index=True)
    network = Column(String)
    version = Column(String)
    city = Column(String)
    region = Column(String)
    region_code = Column(String)
    country = Column(String)
    country_name = Column(String)
    country_code = Column(String)
    country_code_iso3 = Column(String)
    country_capital = Column(String)
    country_tld = Column(String)
    continent_code = Column(String)
    in_eu = Column(Boolean)
    postal = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)
    utc_offset = Column(String)
    country_calling_code = Column(String)
    currency = Column(String)
    currency_name = Column(String)
    languages = Column(String)
    country_area = Column(Float)
    country_population = Column(Integer)
    asn = Column(String)
    org = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())