from collections import defaultdict
from importlib.metadata import files
import logging
import os
import re

import cv2

from app.utils.image_variants import ImageVariants
from app.utils.number_plate_parser import NumberPlateParser
from app.services.ocr_model import get_model

logger = logging.getLogger(__name__)


class PlateReader:

    @staticmethod
    def calculate_score(vehicle, text, confidence):

        score = confidence * 100

        if vehicle:
            score += 20

        if vehicle and 8 <= len(vehicle) <= 12:
            score += 10

        # Standard Indian Plate
        if vehicle and re.fullmatch(
            r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}",
            vehicle,
        ):
            score += 20

        # Bharat Series
        if vehicle and re.fullmatch(
            r"[0-9]{2}BH[0-9]{4}[A-Z]{1,2}",
            vehicle,
        ):
            score += 20

        return score

    @staticmethod
    def clean_text(text):

        text = (
            text.upper()
            .replace("IND", "")
            .replace(" ", "")
            .replace("-", "")
            .replace(".", "")
            .replace("\n", "")
            .strip()
        )

        return text

    @staticmethod
    def run_ocr(image_path, source):

        model = get_model()

        results = model.predict(
            input=image_path
        )

        candidates = []

        for res in results:

            text = PlateReader.clean_text(
                res.get(
                    "rec_text",
                    "",
                )
            )
            confidence = res.get(
                "rec_score",
                0,
            )
            vehicle = NumberPlateParser.parse(
                text
            )

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
                    "source": source,
                }
            )

        return candidates

    @staticmethod
    def merge_two_line_candidates(candidates):

        top = None
        bottom = None

        for candidate in candidates:

            if candidate["source"] == "top":
                top = candidate["ocr_text"]

            elif candidate["source"] == "bottom":
                bottom = candidate["ocr_text"]

        if not top or not bottom:

            return None

        top = (
            top.upper()
            .replace("IND", "")
            .replace(" ", "")
            .replace("-", "")
        )

        bottom = (
            bottom.upper()
            .replace("IND", "")
            .replace(" ", "")
            .replace("-", "")
        )

        combinations = [

            top + bottom,

            top + bottom.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),

            top.rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + bottom,

            top.replace("IND", "") + bottom,

            top + bottom.replace("IND", ""),

        ]

        checked = set()

        for merged in combinations:

            merged = merged.strip()

            if not merged:
                continue

            if merged in checked:
                continue

            checked.add(merged)

            vehicle = NumberPlateParser.parse(
                merged
            )

            if vehicle:

                return {
                    "vehicle": vehicle,
                    "ocr_text": merged,
                    "confidence": 1.0,
                    "score": 999,
                    "source": "merged",
                }

        return None

    @staticmethod
    def split_image(image_path):

        image = cv2.imread(image_path)

        if image is None:
            return []

        h, w = image.shape[:2]

        output_dir = os.path.dirname(image_path)

        files = []

        whole_path = os.path.join(
            output_dir,
            "ocr_whole.jpg",
        )

        cv2.imwrite(
            whole_path,
            image,
        )

        files.append(
            ("whole", whole_path)
        )

        top = image[
            0:int(h * 0.55),
            :
        ]

        top_path = os.path.join(
            output_dir,
            "ocr_top.jpg",
        )

        cv2.imwrite(
            top_path,
            top,
        )

        files.append(
            ("top", top_path)
        )

        bottom = image[
            int(h * 0.40):,
            :
        ]

        bottom_path = os.path.join(
            output_dir,
            "ocr_bottom.jpg",
        )

        cv2.imwrite(
            bottom_path,
            bottom,
        )

        files.append(
            ("bottom", bottom_path)
        )

        left = image[
            :,
            0:int(w * 0.55)
        ]

        left_path = os.path.join(
            output_dir,
            "ocr_left.jpg",
        )

        cv2.imwrite(
            left_path,
            left,
        )

        files.append(
            ("left", left_path)
        )

        right = image[
            :,
            int(w * 0.45):
        ]

        right_path = os.path.join(
            output_dir,
            "ocr_right.jpg",
        )

        cv2.imwrite(
            right_path,
            right,
        )

        files.append(
            ("right", right_path)
        )

        cx1 = int(w * 0.10)
        cx2 = int(w * 0.90)

        center = image[
            :,
            cx1:cx2,
        ]

        center_path = os.path.join(
            output_dir,
            "ocr_center.jpg",
        )

        cv2.imwrite(
            center_path,
            center,
        )

        files.append(
            ("center", center_path)
        )

        top40 = image[
            :int(h * 0.40),
            :
        ]

        top40_path = os.path.join(
            output_dir,
            "ocr_top40.jpg",
        )

        cv2.imwrite(
            top40_path,
            top40,
        )

        files.append(
            ("top40", top40_path)
        )

        bottom60 = image[
            int(h * 0.35):,
            :
        ]

        bottom60_path = os.path.join(
            output_dir,
            "ocr_bottom60.jpg",
        )

        cv2.imwrite(
            bottom60_path,
            bottom60,
        )

        files.append(
            ("bottom60", bottom60_path)
        )

        wide = image[
            int(h * 0.10):int(h * 0.90),
            int(w * 0.05):int(w * 0.95),
        ]

        wide_path = os.path.join(
            output_dir,
            "ocr_wide.jpg",
        )

        cv2.imwrite(
            wide_path,
            wide,
        )

        files.append(
            ("wide", wide_path)
        )
        
        return files

    @staticmethod
    def read(image_path):

        candidates = []

        variants = ImageVariants.generate(
            image_path
        )

        for path in variants:

            candidates.extend(
                PlateReader.run_ocr(
                    path,
                    source=os.path.basename(path),
                )
            )

        split_images = PlateReader.split_image(
            image_path
        )

        for source, path in split_images:

            candidates.extend(
                PlateReader.run_ocr(
                    path,
                    source=source,
                )
            )

        merged = PlateReader.merge_two_line_candidates(
            candidates
        )

        if merged:

            candidates.append(
                merged
            )

        votes = defaultdict(list)

        for candidate in candidates:

            if candidate["vehicle"]:

                votes[
                    candidate["vehicle"]
                ].append(candidate)

        if not votes:

            logger.warning(
                "No valid vehicle number detected."
            )

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
                sum(
                    i["score"]
                    for i in items
                )
                / vote_count
            )

            max_confidence = max(
                i["confidence"]
                for i in items
            )


            if (

                vote_count > highest_vote

                or

                (
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