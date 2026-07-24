from collections import defaultdict
import logging
import re

# from paddleocr import TextRecognition

from app.utils.image_variants import ImageVariants
from app.utils.number_plate_parser import NumberPlateParser

logger = logging.getLogger(__name__)

# model = TextRecognition(engine="paddle")
from app.services.ocr_model import get_model

class PlateReader:

    @staticmethod
    def calculate_score(vehicle, text, confidence):
        score = confidence * 100

        if vehicle:
            score += 20

        if vehicle and 8 <= len(vehicle) <= 10:
            score += 10

        if vehicle and re.fullmatch(
            r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}",
            vehicle,
        ):
            score += 20

        return score

    @staticmethod
    def read(image_path):

        variants = ImageVariants.generate(image_path)

        candidates = []

        for path in variants:

            model = get_model()
            results = model.predict(input=path)

            text = ""
            confidence = 0

            for res in results:
                text = res.get("rec_text", "")
                confidence = res.get("rec_score", 0)

            text = (
                text.upper()
                .replace(" ", "")
                .replace("-", "")
                .replace(".", "")
            )

            vehicle = NumberPlateParser.parse(text)

            score = PlateReader.calculate_score(
                vehicle,
                text,
                confidence,
            )

            candidates.append(
                {
                    "vehicle": vehicle,
                    "ocr_text": text,
                    "confidence": confidence,
                    "score": score,
                    "variant": path,
                }
            )

        votes = defaultdict(list)

        for candidate in candidates:
            if candidate["vehicle"]:
                votes[candidate["vehicle"]].append(candidate)

        if not votes:
            logger.warning("No valid vehicle number detected.")
            return {
                "vehicle_no": None,
                "ocr_text": "",
                "confidence": 0,
            }

        best_vehicle = None
        best_confidence = 0
        best_text = ""

        highest_vote = -1
        highest_score = -1

        for vehicle, items in votes.items():

            vote_count = len(items)

            average_score = (
                sum(i["score"] for i in items)
                / vote_count
            )

            max_confidence = max(
                i["confidence"]
                for i in items
            )

            if (
                vote_count > highest_vote
                or (
                    vote_count == highest_vote
                    and average_score > highest_score
                )
            ):

                highest_vote = vote_count
                highest_score = average_score

                best_vehicle = vehicle
                best_confidence = max_confidence

                best_text = max(
                    items,
                    key=lambda x: x["score"],
                )["ocr_text"]

        logger.info(
            "Vehicle detected: %s (%.2f%%)",
            best_vehicle,
            best_confidence * 100,
        )

        return {
            "vehicle_no": best_vehicle,
            "ocr_text": best_text,
            "confidence": round(
                best_confidence * 100,
                2,
            ),
        }