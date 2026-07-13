from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class UploadedImage(Base):
    __tablename__ = "uploaded_images"

    id = Column(Integer, primary_key=True, index=True)

    original_name = Column(String(255), nullable=False)

    stored_name = Column(String(255), nullable=False)

    image_path = Column(String(500), nullable=False)

    ocr_status = Column(
        String(20),
        default="PENDING"
    )

    ocr_text = Column(String(100))

    confidence = Column(String(20))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )