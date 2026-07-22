from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.models.gate_pass import GatePass
from app.models.uploaded_image import UploadedImage


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session):

        total_vehicles = (
            db.query(func.count(Vehicle.id)).scalar() or 0
        )

        total_gate_passes = (
            db.query(func.count(GatePass.id)).scalar() or 0
        )

        gate_pass_today = (
            db.query(func.count(GatePass.id))
            .filter(func.date(GatePass.entry_time) == date.today())
            .scalar()
            or 0
        )

        confidence_values = (
            db.query(UploadedImage.confidence)
            .filter(UploadedImage.confidence.isnot(None))
            .all()
        )

        valid_confidence = []

        for value in confidence_values:
            try:
                valid_confidence.append(float(value[0]))
            except (TypeError, ValueError):
                continue

        ocr_accuracy = (
            round(sum(valid_confidence) / len(valid_confidence), 2)
            if valid_confidence
            else 0
        )

        return {
            "summary": {
                "total_vehicles": total_vehicles,
                "gate_pass_today": gate_pass_today,
                "total_gate_passes": total_gate_passes,
                "ocr_accuracy": ocr_accuracy,
                "system_status": "Online",
            }
        }