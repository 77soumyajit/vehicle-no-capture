from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.vehicle import router as vehicle_router
from app.database.database import Base, engine

# Import models so SQLAlchemy registers them
import app.models

app = FastAPI(
    title="Vehicle Gate Pass API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicle_router)

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Vehicle Gate Pass API Running"
    }