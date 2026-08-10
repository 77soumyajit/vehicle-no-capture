# from sqlalchemy.orm import Session

# from app.services.upload_service import UploadService
# from app.ai.detector import PlateDetector


# class LiveDetectService:

#     @staticmethod
#     def detect(db: Session, image):

#         # Upload image
#         uploaded = UploadService.upload_image(
#             db,
#             image,
#         )

#         # Run YOLO
#         results = PlateDetector.detect(
#             uploaded.image_path
#         )

#         best_confidence = 0.0

#         for result in results:

#             if result.boxes is None:
#                 continue

#             if len(result.boxes) == 0:
#                 continue

#             for box in result.boxes:

#                 confidence = float(box.conf[0])

#                 if confidence > best_confidence:
#                     best_confidence = confidence

#         if best_confidence > 0:

#             return {

#                 "status": "PLATE_FOUND",

#                 "plate_detected": True,

#                 "confidence": round(best_confidence * 100, 2),

#                 "image_id": uploaded.id,

#                 "image_path": uploaded.image_path,

#             }

#         return {

#             "status": "PLATE_NOT_FOUND",

#             "plate_detected": False,

#             "confidence": 0,

#             "image_id": uploaded.id,

#             "image_path": uploaded.image_path,

#         }



import os
import tempfile

from app.ai.detector import PlateDetector


class LiveDetectService:

    @staticmethod
    def detect(image):

        temp_path = None

        try:

            image_data = image.file.read()

            if not image_data:
                return {
                    "status": "INVALID_IMAGE",
                    "plate_detected": False,
                    "confidence": 0,
                }

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            ) as temp_file:

                temp_file.write(image_data)
                temp_path = temp_file.name

            results = PlateDetector.detect(
                temp_path
            )

            best_confidence = 0.0

            for result in results:

                if result.boxes is None:
                    continue

                if len(result.boxes) == 0:
                    continue

                for box in result.boxes:

                    confidence = float(
                        box.conf[0]
                    )

                    if confidence > best_confidence:
                        best_confidence = confidence

            if best_confidence > 0:

                return {
                    "status": "PLATE_FOUND",
                    "plate_detected": True,
                    "confidence": round(
                        best_confidence * 100,
                        2
                    ),
                }

            return {
                "status": "PLATE_NOT_FOUND",
                "plate_detected": False,
                "confidence": 0,
            }

        finally:

            if temp_path and os.path.exists(temp_path):

                try:
                    os.remove(temp_path)

                except OSError:
                    pass