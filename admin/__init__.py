import os

from sqladmin import Admin
from fastapi import FastAPI

from admin.admin_auth import AdminAuth
from db.db_conn import engine
from admin.views import AnalyticsAdmin, UserAdmin, WebsiteAdmin, VisitorAdmin, UserLocationAdmin, DashboardAdmin


def setup_admin(app: FastAPI):
    authentication_backend = AdminAuth(secret_key=os.getenv('SECRET_KEY'))
    admin = Admin(app, engine=engine, authentication_backend=authentication_backend)

    admin.add_view(AnalyticsAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(WebsiteAdmin)
    admin.add_view(VisitorAdmin)
    admin.add_view(UserLocationAdmin)

    admin.add_view(DashboardAdmin)

