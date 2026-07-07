from pydantic import BaseModel


class VehicleResponse(BaseModel):
    id: int
    vehicle_no: str
    owner_name: str
    driver_name: str

    model_config = {
        "from_attributes": True
    }