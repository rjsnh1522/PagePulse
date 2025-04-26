import os

from sqladmin import Admin
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse

from admin.admin_auth import AdminAuth
from db.db_conn import engine
from admin.views import AnalyticsAdmin, UserAdmin, WebsiteAdmin, VisitorAdmin, UserLocationAdmin, DashboardAdmin

class CustomAdmin(Admin):
    async def index(self, request: Request):
        return RedirectResponse(url="/admin/dashboard")


def setup_admin(app: FastAPI):
    authentication_backend = AdminAuth(secret_key=os.getenv('SECRET_KEY'))
    admin = CustomAdmin(app, engine=engine,
                  authentication_backend=authentication_backend,
                  templates_dir='templates')

    admin.add_view(DashboardAdmin)

    admin.add_view(AnalyticsAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(WebsiteAdmin)
    admin.add_view(VisitorAdmin)
    admin.add_view(UserLocationAdmin)



