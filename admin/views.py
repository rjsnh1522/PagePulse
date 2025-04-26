from pydantic_core.core_schema import model_field
from sqladmin import ModelView
from db.models import Analytics, User, Website, Visitor


class AnalyticsAdmin(ModelView, model=Analytics):
    column_list = [
        "event_type", "visitor_id", "visitor_session_id",
        "ipv4", "current_page_url", "platform",
        "device", "session_duration", "timestamp"
    ]
    column_searchable_list = ["visitor_id", "visitor_session_id", "ipv4"]
    column_sortable_list = ["timestamp", "session_duration"]


class UserAdmin(ModelView, model=User):
    column_list = ["id", "name", "email", "is_active", "created_at"]

class WebsiteAdmin(ModelView, model=Website):
    column_list = ["id", "domain", "owner_id", "created_at"]


class VisitorAdmin(ModelView, model=Visitor):
    column_list = ["id", "unique_id", "first_visit", "last_visit"]