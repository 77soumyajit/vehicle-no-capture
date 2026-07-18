from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.services.vehicle_service import VehicleService

router = APIRouter(
    prefix="/vehicle",
    tags=["Vehicle"],
)


@router.get("/{vehicle_no}", response_model=VehicleResponse)
def search_vehicle(
    vehicle_no: str,
    db: Session = Depends(get_db),
):

    vehicle = VehicleService.search_vehicle(
        db,
        vehicle_no,
    )

    if vehicle is None:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    return vehicle


@router.post("/", response_model=VehicleResponse)
def create_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db),
):

    existing = VehicleService.search_vehicle(
        db,
        data.vehicle_no,
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Vehicle already exists",
        )

    return VehicleService.create_vehicle(
        db,
        data,
    )