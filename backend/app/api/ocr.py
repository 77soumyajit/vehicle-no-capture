from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.upload_repository import UploadRepository
from app.services.ocr_service import OCRService

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


@router.post("/detect")
def detect(image_id: int, db: Session = Depends(get_db)):

    image = UploadRepository.get_by_id(db, image_id)

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    result = OCRService.detect_vehicle_number(
        image.image_path
    )

    UploadRepository.update_ocr(
        db,
        image,
        result["vehicle_no"],
        result["confidence"],
    )

    return result