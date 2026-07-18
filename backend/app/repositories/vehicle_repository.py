from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


class VehicleRepository:

    @staticmethod
    def get_by_vehicle_number(db: Session, vehicle_no: str):
        return (
            db.query(Vehicle)
            .filter(Vehicle.vehicle_no == vehicle_no)
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, vehicle_id: int):
        return (
            db.query(Vehicle)
            .filter(Vehicle.id == vehicle_id)
            .first()
        )

    @staticmethod
    def create(db: Session, vehicle: Vehicle):

        db.add(vehicle)

        db.commit()

        db.refresh(vehicle)

        return vehicle