from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- User ----------

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr = Field(max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    role: str
    created_at: datetime


# ---------- Node ----------

class NodeBase(BaseModel):
    node_name: str = Field(min_length=1, max_length=100)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    location_name: str | None = Field(default=None, max_length=150)


class NodeCreate(NodeBase):
    user_id: int


class NodeUpdate(BaseModel):
    node_name: str | None = Field(default=None, min_length=1, max_length=100)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    location_name: str | None = Field(default=None, max_length=150)


class NodeResponse(NodeBase):
    model_config = ConfigDict(from_attributes=True)

    node_id: int
    user_id: int
    status: str
    installed_at: datetime | None
    last_seen: datetime | None


# ---------- Weather Reading ----------

class ReadingBase(BaseModel):
    temperature: Decimal | None = None
    humidity: Decimal | None = None
    pressure: Decimal | None = None
    light_level: Decimal | None = None


class ReadingCreate(ReadingBase):
    node_id: int


class ReadingResponse(ReadingBase):
    model_config = ConfigDict(from_attributes=True)

    reading_id: int
    node_id: int
    recorded_at: datetime


# ---------- Node Diagnostic ----------

class DiagnosticBase(BaseModel):
    uptime: int | None = None
    wifi_connected: bool | None = None
    dht22_status: bool | None = None
    pressure_sensor_status: bool | None = None
    light_sensor_status: bool | None = None
    gps_status: bool | None = None


class DiagnosticCreate(DiagnosticBase):
    node_id: int


class DiagnosticResponse(DiagnosticBase):
    model_config = ConfigDict(from_attributes=True)

    diagnostic_id: int
    node_id: int
    recorded_at: datetime


# ---------- Favourite ----------

class FavouriteCreate(BaseModel):
    node_id: int


class FavouriteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    node_id: int


# ---------- Alert ----------

class AlertBase(BaseModel):
    node_id: int
    measurement_type: str = Field(min_length=1, max_length=50)
    comparison_operator: str = Field(min_length=1, max_length=10)
    threshold_value: Decimal
    enabled: bool = True


class AlertCreate(AlertBase):
    user_id: int


class AlertUpdate(BaseModel):
    measurement_type: str | None = Field(default=None, min_length=1, max_length=50)
    comparison_operator: str | None = Field(default=None, min_length=1, max_length=10)
    threshold_value: Decimal | None = None
    enabled: bool | None = None


class AlertResponse(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    alert_id: int
    user_id: int
    created_at: datetime
