from sqladmin import Admin
from fastapi import FastAPI
from db.db_conn import engine
from admin.views import AnalyticsAdmin, UserAdmin, WebsiteAdmin, VisitorAdmin, UserLocationAdmin, DashboardAdmin


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(AnalyticsAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(WebsiteAdmin)
    admin.add_view(VisitorAdmin)
    admin.add_view(UserLocationAdmin)

    admin.add_view(DashboardAdmin)

