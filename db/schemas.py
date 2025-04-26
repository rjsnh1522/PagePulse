from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class AnalyticsData(BaseModel):
    event_type: str  # "onLoad" or "onExit"
    visitor_id: str
    visitor_session_id: str

    ipv4: Optional[str] = None
    ipv6: Optional[str] = None
    current_page_url: HttpUrl
    current_page_path: str
    referrer: Optional[str] = "Direct"
    platform: str
    device: str
    page_height: int
    scroll_depth: float
    session_duration: int
    timestamp: datetime
    user_agent: str
    browser_primary: str
    browser_secondary: Optional[str] = None
