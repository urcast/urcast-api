from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class WeatherReadingCreate(BaseModel):
    node_id: int
    temperature: Decimal | None = None
    humidity: Decimal | None = None
    pressure: Decimal | None = None
    light_level: Decimal | None = None


class WeatherReadingResponse(WeatherReadingCreate):
    reading_id: int
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)
