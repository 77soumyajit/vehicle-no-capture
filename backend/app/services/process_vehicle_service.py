from sqlalchemy.orm import Session

from app.services.upload_service import UploadService
from app.ai.detector import PlateDetector
from app.ai.crop_plate import PlateCropper
from app.ai.plate_reader import PlateReader
from app.services.vehicle_service import VehicleService


class ProcessVehicleService:

    @staticmethod
    def process(db: Session, image):


        uploaded = UploadService.upload_image(
            db,
            image,
        )

        results = PlateDetector.detect(
            uploaded.image_path
        )



        cropped_path = PlateCropper.crop(
            uploaded.image_path,
            results,
        )


        if cropped_path is None:

        

            return {

                "status": "PLATE_NOT_FOUND",

                "message": "No license plate detected."

            }

        ocr_result = PlateReader.read(
            cropped_path
        )


        vehicle_no = ocr_result.get("vehicle_no")

        if vehicle_no is None:


            return {

                "status": "OCR_FAILED",

                "message": "Unable to detect vehicle number.",

                "confidence": ocr_result.get(
                    "confidence",
                    0,
                ),

            }


        vehicle = VehicleService.search_vehicle(
            db,
            vehicle_no,
        )

        if vehicle:

            return {

                "status": "FOUND",

                "confidence": ocr_result["confidence"],

                "vehicle": {

                    "id": vehicle.id,

                    "vehicle_no": vehicle.vehicle_no,

                    "owner_name": vehicle.owner_name,

                    "driver_name": vehicle.driver_name,

                    "company_name": vehicle.company_name,

                    "vehicle_type": vehicle.vehicle_type,

                    "manufacturer": vehicle.manufacturer,

                    "color": vehicle.color,

                },

            }


        return {

            "status": "NOT_FOUND",

            "vehicle_no": vehicle_no,

            "confidence": ocr_result["confidence"],

        }

