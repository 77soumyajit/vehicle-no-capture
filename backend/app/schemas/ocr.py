from pydantic import BaseModel


class OCRRequest(BaseModel):
    image_id: int


class OCRResponse(BaseModel):
    vehicle_no: str | None
    confidence: float