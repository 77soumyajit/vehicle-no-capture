from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


def get_vehicle_by_number(db: Session, vehicle_no: str):
    return (
        db.query(Vehicle)
        .filter(Vehicle.vehicle_no == vehicle_no)
        .first()
    )