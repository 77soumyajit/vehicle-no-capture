from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.vehicle import router as vehicle_router
from app.api.gate_pass import router as gate_pass_router
from app.api.upload import router as upload_router
from app.api.ocr import router as ocr_router
from app.api.process_vehicle import router as process_vehicle_router
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

# Register Routers
app.include_router(vehicle_router)
app.include_router(gate_pass_router)


@app.get("/")
def home():
    return {
        "message": "Vehicle Gate Pass API Running"
    }

app.include_router(upload_router)
app.include_router(ocr_router)
app.include_router(process_vehicle_router)