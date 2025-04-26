from sqlalchemy.orm import Session
from db.models import Visitor
from sqlalchemy import update
from datetime import datetime, timezone


class VisitorService:
    @staticmethod
    def create_visitor_if_not_exists(unique_id: str, db: Session):
        existing_visitor = db.query(Visitor).filter(Visitor.unique_id == unique_id).first()
        if not existing_visitor:
            new_visitor = Visitor(unique_id=unique_id)
            db.add(new_visitor)
            db.commit()
            db.refresh(new_visitor)
            return new_visitor
        return existing_visitor

    @staticmethod
    def update_last_visit(unique_id: str, db: Session):
        visitor = db.query(Visitor).filter(Visitor.unique_id == unique_id).first()
        if visitor:
            visitor.last_visit = datetime.now(timezone.utc)
            db.commit()
            return visitor
        return None

    @staticmethod
    def get_visitor_by_unique_id(unique_id: str, db: Session):
        return db.query(Visitor).filter(Visitor.unique_id == unique_id).first()
