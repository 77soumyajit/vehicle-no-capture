from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class GatePass(Base):
    __tablename__ = "gate_pass"

    id = Column(Integer, primary_key=True, index=True)

    gate_pass_no = Column(String(30), unique=True, nullable=False)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicle_details.id"),
        nullable=False
    )

    status = Column(
        String(20),
        default="ACTIVE"
    )

    entry_time = Column(
        DateTime,
        server_default=func.now()
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    vehicle = relationship(
    "Vehicle",
    lazy="joined"
)