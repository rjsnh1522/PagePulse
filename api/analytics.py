from fastapi import APIRouter, status, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db.db_conn import get_db
from db.schemas import AnalyticsData
from tasks.bg_tasks import process_analytics
from utils import app_logger

router = APIRouter(prefix="", tags=["track"])
logger = app_logger.createLogger("app")


@app_logger.functionlogs(log="app")
@router.post("/analytics", status_code=status.HTTP_200_OK, name="analytics")
async def track_analytics(data: AnalyticsData,
                          background_tasks: BackgroundTasks,
                          db: Session = Depends(get_db)):
    try:
        logger.info('adding request to background task')
        logger.info(data)
        background_tasks.add_task(process_analytics, data, db)
        logger.info('request added to background task')
    except Exception as e:
        app_logger.exceptionlogs(f"Error before insert: {e}")
    return JSONResponse({"status": "ok"})