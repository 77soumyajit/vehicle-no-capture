from datetime import datetime

from pydantic import BaseModel

from app.schemas.vehicle import VehicleResponse


class GatePassCreate(BaseModel):
    vehicle_id: int


class GatePassResponse(BaseModel):
    id: int
    gate_pass_no: str
    entry_time: datetime
    status: str

    vehicle: VehicleResponse

    model_config = {
        "from_attributes": True
    }