from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.process_vehicle_service import ProcessVehicleService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/process-vehicle",
    tags=["Process Vehicle"],
)


@router.post("/")
def process_vehicle(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ProcessVehicleService.process(
        db,
        image,
    )