import re


VALID_STATES = {
    "AN", "AP", "AR", "AS", "BR", "CG", "CH", "DD",
    "DL", "DN", "GA", "GJ", "HP", "HR", "JH", "JK",
    "KA", "KL", "LA", "LD", "MH", "ML", "MN", "MP",
    "MZ", "NL", "OD", "PB", "PY", "RJ", "SK", "TN",
    "TR", "TS", "UK", "UP", "WB"
}


class IndianPlateValidator:

    PATTERN = re.compile(
        r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$"
    )

    @classmethod
    def is_valid(cls, plate):

        if not plate:
            return False

        if not cls.PATTERN.fullmatch(plate):
            return False

        return plate[:2] in VALID_STATES