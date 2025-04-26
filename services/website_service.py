from sqlalchemy.orm import Session

from db.models import Website


class WebsiteService:

    @staticmethod
    def get_website_by_id(website_id: str, db: Session):
        return db.query(Website).filter(Website.id == website_id).first()

    @staticmethod
    def get_websites_by_owner_id(owner_id: str, db: Session):
        return db.query(Website).filter(Website.owner_id == owner_id).all()
