from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db.db_conn import get_db
from db.schemas import AnalyticsData
from utils import app_logger

router = APIRouter(prefix="", tags=["track"])
logger = app_logger.createLogger("app")


@app_logger.functionlogs(log="app")
@router.post("/analytics", status_code=status.HTTP_200_OK, name="analytics")
async def track_analytics(data: AnalyticsData, db: Session = Depends(get_db)):
    logger.info(f"Data, {data}")
    return JSONResponse({"status": "ok"})