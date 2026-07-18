from pydantic import BaseModel


class VehicleCreate(BaseModel):
    vehicle_no: str
    owner_name: str
    driver_name: str
    company_name: str | None = None
    vehicle_type: str | None = None
    manufacturer: str | None = None
    color: str | None = None


class VehicleResponse(BaseModel):
    id: int
    vehicle_no: str
    owner_name: str
    driver_name: str
    company_name: str | None = None
    vehicle_type: str | None = None
    manufacturer: str | None = None
    color: str | None = None

    model_config = {
        "from_attributes": True
    }