from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.models import Analytics, UserLocation
from services.visitor_service import VisitorService
from services.website_service import WebsiteService
from utils import app_logger
from utils import helper



class UserLocationService:

    @staticmethod
    def save_user_location(analytics_instance, ipv4, db: Session):
        try:
            data = helper.find_country_by_ip(ipv4)
            if not data:
                return False

            user_location = UserLocation(
                ip=data.get("ip") or None,
                analytics_id=analytics_instance,
                network=data.get("network") or None,
                version=data.get("version") or None,
                city=data.get("city") or None,
                region=data.get("region") or None,
                region_code=data.get("region_code") or None,
                country=data.get("country") or None,
                country_name=data.get("country_name") or None,
                country_code=data.get("country_code") or None,
                country_code_iso3=data.get("country_code_iso3") or None,
                country_capital=data.get("country_capital") or None,
                country_tld=data.get("country_tld") or None,
                continent_code=data.get("continent_code") or None,
                in_eu=data.get("in_eu") if data.get("in_eu") is not None else None,
                postal=data.get("postal") or None,
                latitude=data.get("latitude") or None,
                longitude=data.get("longitude") or None,
                timezone=data.get("timezone") or None,
                utc_offset=data.get("utc_offset") or None,
                country_calling_code=data.get("country_calling_code") or None,
                currency=data.get("currency") or None,
                currency_name=data.get("currency_name") or None,
                languages=data.get("languages") or None,
                country_area=data.get("country_area") or None,
                country_population=data.get("country_population") or None,
                asn=data.get("asn") or None,
                org=data.get("org") or None
            )
            db.add(user_location)
            db.commit()
            db.refresh(user_location)
            return user_location
        except Exception as e:
            app_logger.exceptionlogs(f"Error in save user location, Error: {e}")
            return None




class AnalyticsService:

    @staticmethod
    def create_or_update_record(data, db: Session):
        if data.event_type == "onExit":
            analytics_updated = AnalyticsService.update_on_exit_analytics_record(data=data, db=db)
        else:
            analytics_created = AnalyticsService.create_on_load_analytics_record(data=data, db=db)

    @staticmethod
    def create_on_load_analytics_record(data, db: Session):
        try:
            visitor_id = data.visitor_id
            website_id = data.website_id
            visitor = VisitorService.create_visitor_if_not_exists(unique_id=visitor_id, db=db)
            website = WebsiteService.get_website_by_id(website_id=website_id, db=db)

            if not website:
                raise Exception(f"Invalid domain_id, website not found, {website_id}")

            # Create analytics record
            analytics_record = Analytics(
                website_id=website.id,
                visitor_id=visitor.id,
                visitor_session_id=data.visitor_session_id,
                page_url=str(data.current_page_url),
                current_page_path=data.current_page_path,
                domain_name=data.domain_name,
                referrer=data.referrer,
                landing_page=str(data.current_page_url),  # Assuming landing_page is same as page_url onLoad
                session_duration=data.session_duration,
                scroll_depth=data.scroll_depth,
                ip=data.ipv4,
                ipv6=data.ipv6,
                user_agent=data.user_agent,
                browser=data.browser_primary,
                browser_secondary=data.browser_secondary,
                device=data.device,
                page_height=data.page_height,
                platform=data.platform,
                timestamp=data.timestamp
            )
            db.add(analytics_record)
            db.commit()
            db.refresh(analytics_record)

            UserLocationService.save_user_location(analytics_instance=analytics_record.id, ipv4=data.ipv4, db=db)

            return analytics_record
        except Exception as e:
            app_logger.exceptionlogs(f"Error in create_on_load_analytics_record Error: {e}")
            return None

    @staticmethod
    def update_on_exit_analytics_record(data, db: Session):
        try:
            website = WebsiteService.get_website_by_id(website_id=data.website_id, db=db)

            visitor_session_id = data.visitor_session_id
            existing_record = db.query(Analytics).filter(
                Analytics.visitor_session_id == data.visitor_session_id
            ).order_by(Analytics.timestamp.desc()).first()

            if not existing_record:
                raise Exception("No existing session found to update.")

            # Update session_duration, scroll_depth, and timestamp
            existing_record.session_duration = data.session_duration
            existing_record.scroll_depth = data.scroll_depth
            existing_record.timestamp = data.timestamp  # Use exit timestamp

            db.commit()
            db.refresh(existing_record)
            return existing_record

        except Exception as e:
            app_logger.exceptionlogs(f"Error in update_on_exit_analytics_record Error: {e}")
            return None