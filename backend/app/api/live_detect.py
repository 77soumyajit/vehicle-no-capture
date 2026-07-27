from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.live_detect_service import LiveDetectService


router = APIRouter(
    prefix="/live-detect",
    tags=["Live Detection"],
)


@router.post("/")
async def detect_live_vehicle(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    return LiveDetectService.detect(
        db=db,
        image=image,
    )