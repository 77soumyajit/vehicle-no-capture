from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.models.gate_pass import GatePass
from app.models.uploaded_image import UploadedImage


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session):

        today = date.today()

        total_vehicles = (
            db.query(func.count(Vehicle.id))
            .scalar()
            or 0
        )

        registered_today = (
            db.query(func.count(Vehicle.id))
            .filter(
                func.date(Vehicle.created_at) == today
            )
            .scalar()
            or 0
        )

        total_gate_passes = (
            db.query(func.count(GatePass.id))
            .scalar()
            or 0
        )

        gate_pass_today = (
            db.query(func.count(GatePass.id))
            .filter(
                func.date(GatePass.entry_time) == today
            )
            .scalar()
            or 0
        )

        total_images = (
            db.query(func.count(UploadedImage.id))
            .scalar()
            or 0
        )

        images_processed_today = (
            db.query(func.count(UploadedImage.id))
            .filter(
                func.date(
                    UploadedImage.created_at
                ) == today
            )
            .scalar()
            or 0
        )

        confidence_values = (
            db.query(
                UploadedImage.confidence
            )
            .filter(
                UploadedImage.confidence.isnot(None)
            )
            .all()
        )

        valid_confidence = []

        for value in confidence_values:

            try:
                valid_confidence.append(
                    float(value[0])
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

        ocr_accuracy = (
            round(
                sum(valid_confidence)
                / len(valid_confidence),
                2,
            )
            if valid_confidence
            else 0
        )

        return {

            "summary": {

                "registered_today": registered_today,

                "gate_pass_today": gate_pass_today,

                "images_processed_today": images_processed_today,

                "total_vehicles": total_vehicles,

                "total_gate_passes": total_gate_passes,

                "total_images": total_images,

                "ocr_accuracy": ocr_accuracy,

                "system_status": "Online",

            }

        }