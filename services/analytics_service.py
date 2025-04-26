from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.models import Analytics


class AnalyticsService:

    @staticmethod
    def create_or_update_record(data, db: Session):
        if data.event_type == "onExit":
            visitor_session_id = data.visitor_session_id
            AnalyticsService.update_on_exit_analytics_record(data=data, db=db)
        else:
            AnalyticsService.create_on_load_analytics_record(data=data, db=db)

    @staticmethod
    def create_on_load_analytics_record(data, db: Session):
        pass

    @staticmethod
    def update_on_exit_analytics_record(data, db: Session):

        existing_record = db.query(Analytics).filter(
            Analytics.visitor_session_id == data.visitor_session_id
        ).order_by(desc(Analytics.timestamp)).first()