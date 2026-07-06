from fastapi import APIRouter

router = APIRouter(
    prefix="/vehicle",
    tags=["Vehicle"]
)


@router.get("/")
def get_vehicle():
    return {
        "status": "success",
        "message": "Vehicle API is working!",
        "vehicle": {
            "vehicle_no": "OD02AB1234",
            "owner_name": "ABC Logistics",
            "driver_name": "Ramesh Kumar"
        }
    }