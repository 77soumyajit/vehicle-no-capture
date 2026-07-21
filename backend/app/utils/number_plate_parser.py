import re

from app.utils.indian_plate_validator import IndianPlateValidator


LETTER_FIX = {
    "0": "O",
    "1": "I",
    "2": "Z",
    "5": "S",
    "8": "B",
}


DIGIT_FIX = {
    "O": "0",
    "I": "1",
    "Z": "2",
    "S": "5",
    "B": "8",
}


class NumberPlateParser:

    @staticmethod
    def clean(text):

        return (
            text.upper()
            .replace(" ", "")
            .replace("-", "")
            .replace(".", "")
        )

    @staticmethod
    def fix_letters(text):

        result = ""

        for ch in text:
            result += LETTER_FIX.get(ch, ch)

        return result

    @staticmethod
    def fix_digits(text):

        result = ""

        for ch in text:
            result += DIGIT_FIX.get(ch, ch)

        return result

    @staticmethod
    def parse(text):

        if not text:
            return None

        text = NumberPlateParser.clean(text)

        # -----------------------------
        # If OCR is already correct,
        # NEVER modify it.
        # -----------------------------

        if IndianPlateValidator.is_valid(text):
            return text

        # -----------------------------
        # Find last 3 or 4 digits
        # -----------------------------

        match = re.search(r"(\d{3,4})$", text)

        if not match:
            return None

        number = match.group()

        prefix = text[:-len(number)]

        if len(prefix) < 5:
            return None

        state = prefix[:2]

        district = ""

        series = ""

        for ch in prefix[2:]:

            if ch.isdigit():

                district += ch

            else:

                series += ch

        state = NumberPlateParser.fix_letters(state)

        district = NumberPlateParser.fix_digits(district)

        series = NumberPlateParser.fix_letters(series)

        number = NumberPlateParser.fix_digits(number)

        candidate = (
            state +
            district +
            series +
            number
        )

        if IndianPlateValidator.is_valid(candidate):

            return candidate

        return None