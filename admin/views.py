from pydantic_core.core_schema import model_field
from sqladmin import ModelView, BaseView, expose
from db.models import Analytics, User, Website, Visitor, UserLocation


class DashboardAdmin(BaseView):
    name = "Dashboard"
    icon = "fa-solid fa-chart-line"

    @expose("/dashboard", methods=["GET"])
    async def report_page(self, request):
        return await self.templates.TemplateResponse(request, "dashboard.html")




class AnalyticsAdmin(ModelView, model=Analytics):
    icon = "fa-solid fa-chart-line"
    column_list = [
        "event_type", "visitor_id", "visitor_session_id",
        "ip", "ipv6", "page_url", "platform",
        "referrer",
        "device", "session_duration", "scroll_depth", "country", "browser", "timestamp"
    ]
    column_searchable_list = ["visitor_id", "visitor_session_id", "ip"]
    column_sortable_list = ["timestamp", "session_duration"]


class UserAdmin(ModelView, model=User):
    column_list = ["id", "name", "email", "is_active", "created_at"]

class WebsiteAdmin(ModelView, model=Website):
    column_list = ["id", "domain", "owner_id", "created_at"]


class VisitorAdmin(ModelView, model=Visitor):
    column_list = ["id", "unique_id", "first_visit", "last_visit"]


class UserLocationAdmin(ModelView, model=UserLocation):
    column_list = [
        "id", "analytics_id", "ip",
        "network", "version", "city", "region",
        "region_code", "country", "country_name", "country_code",
        "postal", "latitude", "longitude"]


