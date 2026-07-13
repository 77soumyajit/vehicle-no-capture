import easyocr
import re

reader = easyocr.Reader(["en"])


class OCRService:

    @staticmethod
    def detect_vehicle_number(image_path):

        results = reader.readtext(image_path)

        pattern = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"

        best_match = None
        best_confidence = 0

        for result in results:

            _, text, confidence = result

            text = text.replace(" ", "").upper()

            if re.fullmatch(pattern, text):

                if confidence > best_confidence:

                    best_match = text
                    best_confidence = confidence

        return {
            "vehicle_no": best_match,
            "confidence": round(best_confidence * 100, 2)
        }