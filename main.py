from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.routes import router as api_router
from database import Base, SessionLocal, engine
from frontend.routes import error_response, router as frontend_router
from models import SensorReading

BASE_DIR = Path(__file__).resolve().parent

INITIAL_READINGS = [
    {"sensor": "temp", "content": 21.0, "date_timestamp": datetime(2026, 9, 24, 11, 30)},
    {"sensor": "lux", "content": 100.0, "date_timestamp": datetime(2026, 9, 24, 11, 33)},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialise the SQL database: create tables and seed sample data if empty.
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalars(select(SensorReading)).first() is None:
            db.add_all(SensorReading(**reading) for reading in INITIAL_READINGS)
            db.commit()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend" / "static"), name="static")
app.include_router(frontend_router)
app.include_router(api_router)


# Friendly HTML error pages (JSON is kept for /api/ routes)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    return error_response(request, exc.status_code, str(exc.detail))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": exc.errors()}, status_code=422)
    return error_response(request, 422, "The request could not be processed.")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return error_response(request, status.HTTP_500_INTERNAL_SERVER_ERROR, "An unexpected error occurred. Please try again later.")
