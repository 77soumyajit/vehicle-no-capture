from sqlalchemy.orm import Session

from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:

    @staticmethod
    def search_vehicle(db: Session, vehicle_no: str):
        return VehicleRepository.get_by_vehicle_number(
            db,
            vehicle_no
        )