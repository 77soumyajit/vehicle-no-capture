import re

from app.utils.indian_plate_validator import IndianPlateValidator


LETTER_FIX = {
    "0": "O",
    "1": "I",
    "5": "S",
    "8": "B",
}

DIGIT_FIX = {
    "O": "0",
    "Q": "0",
    "D": "0",
    "I": "1",
    "L": "1",
    "Z": "2",
    "S": "5",
    "B": "8",
}


class NumberPlateParser:

    @staticmethod
    def clean(text):

        if not text:
            return ""

        cleaned = (
            text.upper()
            .replace(" ", "")
            .replace("-", "")
            .replace(".", "")
        )
        return cleaned

    @staticmethod
    def fix_letter(text):

        return "".join(
            LETTER_FIX.get(ch, ch)
            for ch in text
        )

    @staticmethod
    def fix_digit(text):

        return "".join(
            DIGIT_FIX.get(ch, ch)
            for ch in text
        )


    @staticmethod
    def parse_bharat(text):

        pattern = re.compile(
            r"(\d{2})BH([A-Z0-9]{4})([A-Z0-9]{1,2})"
        )

        match = pattern.search(text)

        if not match:
            return None

        year = NumberPlateParser.fix_digit(
            match.group(1)
        )

        serial = NumberPlateParser.fix_digit(
            match.group(2)
        )

        suffix = NumberPlateParser.fix_letter(
            match.group(3)
        )

        candidate = (
            year
            + "BH"
            + serial
            + suffix
        )

        return candidate


    @staticmethod
    def parse_standard(text):

        pattern = re.compile(
            r"([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{3,4})"
        )

        match = pattern.search(text)

        if not match:
            return None

        state = NumberPlateParser.fix_letter(
            match.group(1)
        )

        district = NumberPlateParser.fix_digit(
            match.group(2)
        )

        series = NumberPlateParser.fix_letter(
            match.group(3)
        )

        number = NumberPlateParser.fix_digit(
            match.group(4)
        )

        candidate = (
            state
            + district
            + series
            + number
        )

        if IndianPlateValidator.is_valid(candidate):
            return candidate

        return None

    @staticmethod
    def parse(text):

        text = NumberPlateParser.clean(text)

        if not text:
            return None

        # Already valid

        if IndianPlateValidator.is_valid(text):

            return text

        # Bharat Series

        bharat = NumberPlateParser.parse_bharat(text)

        if bharat:

            return bharat

        # Standard

        standard = NumberPlateParser.parse_standard(text)

        if standard:

            return standard

        return None