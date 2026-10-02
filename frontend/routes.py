from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from frontend.templates import templates
from models import SensorReading

router = APIRouter()


@router.get("/", include_in_schema=False, name="home")
@router.get("/sensor_readings", include_in_schema=False, name="sensor_readings")
def home(request: Request, db: Session = Depends(get_db)):
    readings = db.scalars(select(SensorReading).order_by(SensorReading.id)).all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"readings": [reading.to_dict() for reading in readings], "title": "Sensor Readings"},
    )


@router.get("/sensor_reading/{sensor_reading_id}", include_in_schema=False, name="sensor_reading")
def sensor_reading_page(request: Request, sensor_reading_id: int, db: Session = Depends(get_db)):
    sensor_reading = db.get(SensorReading, sensor_reading_id)
    if sensor_reading is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This sensor reading was not found.",
        )
    return templates.TemplateResponse(
        request,
        "sensor_reading.html",
        {"sensor_reading": sensor_reading.to_dict(), "title": sensor_reading.sensor[:50]},
    )


# Friendly HTML error pages (JSON is kept for /api/ routes)
ERROR_TITLES = {
    400: "Bad Request",
    403: "Forbidden",
    404: "Page Not Found",
    405: "Method Not Allowed",
    422: "Invalid Request",
    500: "Something Went Wrong",
}


def error_response(request: Request, status_code: int, message: str = ""):
    title = ERROR_TITLES.get(status_code, f"Error {status_code}")
    return templates.TemplateResponse(
        request,
        "error.html",
        {"status_code": status_code, "error_title": title, "message": message, "title": title},
        status_code=status_code,
    )
