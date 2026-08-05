import re


VALID_STATES = {
    "AN","AP","AR","AS","BR","CG","CH","DD",
    "DL","DN","GA","GJ","HP","HR","JH","JK",
    "KA","KL","LA","LD","MH","ML","MN","MP",
    "MZ","NL","OD","PB","PY","RJ","SK","TN",
    "TR","TS","UK","UP","WB"
}


class IndianPlateValidator:

    STANDARD = re.compile(
        r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$"
    )

    BH = re.compile(
        r"^\d{2}BH\d{4}[A-Z]{1,2}$"
    )

    @classmethod
    def is_valid(cls, plate):

        if not plate:
            return False

        # Bharat Series
        if cls.BH.fullmatch(plate):
            return True

        # Standard plates
        if cls.STANDARD.fullmatch(plate):
            return plate[:2] in VALID_STATES

        return False    