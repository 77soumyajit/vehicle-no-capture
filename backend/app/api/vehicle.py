from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.vehicle import VehicleResponse
from app.services.vehicle_service import get_vehicle_by_number

router = APIRouter(
    prefix="/vehicle",
    tags=["Vehicle"],
)


@router.get("/{vehicle_no}", response_model=VehicleResponse)
def search_vehicle(vehicle_no: str, db: Session = Depends(get_db)):
    vehicle = get_vehicle_by_number(db, vehicle_no)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    return vehicle