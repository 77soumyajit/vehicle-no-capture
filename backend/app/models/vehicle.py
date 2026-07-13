from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Vehicle(Base):
    __tablename__ = "vehicle_details"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_no = Column(String(20), unique=True, nullable=False)

    owner_name = Column(String(100), nullable=False)

    driver_name = Column(String(100), nullable=False)

    company_name = Column(String(100), nullable=True)

    vehicle_type = Column(String(50), nullable=True)

    manufacturer = Column(String(100), nullable=True)

    color = Column(String(50), nullable=True)