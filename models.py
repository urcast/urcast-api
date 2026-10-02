from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor: Mapped[str] = mapped_column(String(50), index=True)
    content: Mapped[float] = mapped_column(Float)
    date_timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sensor": self.sensor,
            "content": self.content,
            "date_timestamp": self.date_timestamp.strftime("%b %d, %Y, %H:%M"),
        }
