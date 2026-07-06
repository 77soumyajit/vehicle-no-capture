from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.vehicle import router as vehicle_router

app = FastAPI(
    title="Vehicle Gate Pass API",
    version="1.0.0"
)

# Allow React to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicle_router)


@app.get("/")
def home():
    return {
        "message": "Vehicle Gate Pass API Running"
    }