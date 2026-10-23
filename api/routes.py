from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.schemas import WeatherReadingCreate, WeatherReadingResponse
from database import get_db
from models import WeatherReading, Node

router = APIRouter(prefix="/api", tags=["weather-readings"])


@router.get("/weather_readings", response_model=list[WeatherReadingResponse])
def get_weather_readings(db: Session = Depends(get_db)):
    readings = db.scalars(select(WeatherReading).order_by(WeatherReading.reading_id)).all()
    return readings


@router.post("/weather_readings", response_model=WeatherReadingResponse,
             status_code=status.HTTP_201_CREATED)
def create_weather_reading(reading: WeatherReadingCreate, db: Session = Depends(get_db)):
    node = db.get(Node, reading.node_id)
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found."
        )
    weather_reading = WeatherReading(
        node_id=reading.node_id,
        temperature=reading.temperature,
        humidity=reading.humidity,
        pressure=reading.pressure,
        light_level=reading.light_level
    )
    db.add(weather_reading)
    db.commit()
    db.refresh(weather_reading)
    return weather_reading

@router.get("/weather_reading/{reading_id}", response_model=WeatherReadingResponse)
def get_weather_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = db.get(WeatherReading, reading_id)
    if reading is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather reading not found."
        )
    return reading
