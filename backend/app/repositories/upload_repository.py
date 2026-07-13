from sqlalchemy.orm import Session

from app.models.uploaded_image import UploadedImage


class UploadRepository:

    @staticmethod
    def create(db: Session, image: UploadedImage):
        db.add(image)
        db.commit()
        db.refresh(image)
        return image

    @staticmethod
    def get_by_id(db: Session, image_id: int):
        return (
            db.query(UploadedImage)
            .filter(UploadedImage.id == image_id)
            .first()
        )

    @staticmethod
    def update_ocr(
        db: Session,
        image: UploadedImage,
        text: str,
        confidence: float,
    ):
        image.ocr_text = text
        image.confidence = str(confidence)
        image.ocr_status = "COMPLETED"

        db.commit()
        db.refresh(image)

        return image