from pydantic import BaseModel


class SensorReadingCreate(BaseModel):
    sensor: str
    content: float
