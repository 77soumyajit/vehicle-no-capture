from collections import defaultdict
import re

from paddleocr import TextRecognition

from app.utils.image_variants import ImageVariants
from app.utils.number_plate_parser import NumberPlateParser

model = TextRecognition(engine="paddle")


class PlateReader:

    @staticmethod
    def calculate_score(vehicle, text, confidence):
        """
        Calculate a score for an OCR result.
        Higher score = more trustworthy.
        """

        score = confidence * 100

        # Successfully parsed
        if vehicle:
            score += 20

        # Expected Indian number plate length
        if vehicle and 8 <= len(vehicle) <= 10:
            score += 10

        # Matches Indian registration pattern
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

            results = model.predict(input=path)
            print("\n========== RAW OCR ==========")
            print(results)
            print("=============================\n")
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

            print(
                f"{path} -> "
                f"OCR={text} "
                f"Parsed={vehicle} "
                f"Conf={confidence:.3f} "
                f"Score={score:.2f}"
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

        # ------------------------------------------
        # Voting System
        # ------------------------------------------

        votes = defaultdict(list)

        for candidate in candidates:

            if candidate["vehicle"]:

                votes[candidate["vehicle"]].append(candidate)

        if not votes:

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

        print("\n========== OCR Voting ==========")

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

            print(
                f"{vehicle}"
                f" | Votes={vote_count}"
                f" | AvgScore={average_score:.2f}"
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

        print("===============================\n")

        return {

            "vehicle_no": best_vehicle,

            "ocr_text": best_text,

            "confidence": round(
                best_confidence * 100,
                2,
            ),

        }