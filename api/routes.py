from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.schemas import SensorReadingCreate
from database import get_db
from models import SensorReading

router = APIRouter(prefix="/api", tags=["sensor-readings"])


@router.get("/sensor_readings")
def get_sensor_readings(db: Session = Depends(get_db)):
    readings = db.scalars(select(SensorReading).order_by(SensorReading.id)).all()
    return [reading.to_dict() for reading in readings]


@router.post("/sensor_readings", status_code=status.HTTP_201_CREATED)
def create_sensor_reading(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    sensor_reading = SensorReading(sensor=reading.sensor, content=reading.content)
    db.add(sensor_reading)
    db.commit()
    db.refresh(sensor_reading)
    return sensor_reading.to_dict()


@router.get("/sensor_reading/{sensor_reading_id}")
def get_sensor_reading(sensor_reading_id: int, db: Session = Depends(get_db)):
    sensor_reading = db.get(SensorReading, sensor_reading_id)
    if sensor_reading is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This sensor reading was not found.",
        )
    return sensor_reading.to_dict()
