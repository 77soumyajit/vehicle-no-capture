from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.upload_service import UploadService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/image")
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return UploadService.upload_image(
        db,
        file
    )