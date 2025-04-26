from sqlalchemy.orm import Session

from db.schemas import AnalyticsData
from services.analytics_service import AnalyticsService
from services.validator_service import ValidatorService
from utils import app_logger
from utils.app_logger import createLogger

logger = createLogger("app")



def process_analytics(data: AnalyticsData, db: Session):
    try:
        website_exists = ValidatorService.validate_domain_id(website_id=data.website_id, db=db)
        if not website_exists:
            logger.info(f"Website id {data.website_id} doesn't exists")
            return False
        AnalyticsService.create_or_update_record(data=data, db=db)
    except Exception as e:
        app_logger.exceptionlogs(f"Error processing analytics: {e}")