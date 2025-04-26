from sqlalchemy.orm import Session

from db.schemas import AnalyticsData
from services.analytics_service import AnalyticsService
from utils import app_logger


def process_analytics(data: AnalyticsData, db: Session):
    try:
        AnalyticsService.create_or_update_record(data=data, db=db)
    except Exception as e:
        app_logger.exceptionlogs(f"Error processing analytics: {e}")