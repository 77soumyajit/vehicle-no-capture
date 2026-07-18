from pydantic import BaseModel


class ProcessVehicleResponse(BaseModel):

    status: str

    vehicle: dict | None = None

    vehicle_no: str | None = None

    message: str | None = None