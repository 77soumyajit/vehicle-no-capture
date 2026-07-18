from paddleocr import TextRecognition

from app.utils.image_variants import ImageVariants
from app.utils.number_plate_parser import NumberPlateParser

model = TextRecognition(engine="paddle")


class PlateReader:

    @staticmethod
    def read(image_path):

        variants = ImageVariants.generate(
            image_path
        )

        best_vehicle = None
        best_confidence = 0
        best_text = ""


        for path in variants:

            

            results = model.predict(
                input=path
            )

            text = ""
            confidence = 0

            for res in results:

                text = res.get(
                    "rec_text",
                    ""
                )

                confidence = res.get(
                    "rec_score",
                    0
                )

            text = (
                text.upper()
                .replace(" ", "")
                .replace("-", "")
                .replace(".", "")
            )


            vehicle = NumberPlateParser.parse(
                text
            )

            if vehicle and confidence > best_confidence:

                best_vehicle = vehicle
                best_confidence = confidence
                best_text = text

        return {

            "vehicle_no": best_vehicle,

            "ocr_text": best_text,

            "confidence": round(
                best_confidence * 100,
                2
            )

        }