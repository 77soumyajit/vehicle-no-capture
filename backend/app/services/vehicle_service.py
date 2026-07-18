from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:

    @staticmethod
    def search_vehicle(db: Session, vehicle_no: str):
        return VehicleRepository.get_by_vehicle_number(
            db,
            vehicle_no,
        )

    @staticmethod
    def create_vehicle(db: Session, data):

        vehicle = Vehicle(

            vehicle_no=data.vehicle_no,

            owner_name=data.owner_name,

            driver_name=data.driver_name,

            company_name=data.company_name,

            vehicle_type=data.vehicle_type,

            manufacturer=data.manufacturer,

            color=data.color,

        )

        return VehicleRepository.create(
            db,
            vehicle,
        )