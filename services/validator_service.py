from sqlalchemy.orm import Session

from services.website_service import WebsiteService


class ValidatorService:

    @staticmethod
    def validate_domain_id(website_id, db: Session):
        return WebsiteService.get_website_by_id(website_id=website_id, db=db)