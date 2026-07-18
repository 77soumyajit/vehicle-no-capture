import re


class NumberPlateParser:

    @staticmethod
    def parse(text: str):

        if not text:
            return None

        # -----------------------
        # Step 1 : Clean
        # -----------------------
        text = (
            text.upper()
            .replace(" ", "")
            .replace("-", "")
            .replace(".", "")
        )


        chars = list(text)

        # -----------------------
        # Step 2 : Fix State Code
        # First 2 characters must be letters
        # -----------------------

        for i in range(min(2, len(chars))):

            if chars[i] == "0":
                chars[i] = "O"

            elif chars[i] == "1":
                chars[i] = "I"

            elif chars[i] == "8":
                chars[i] = "B"

        # -----------------------
        # Step 3 : District Number
        # Next 2 characters must be digits
        # -----------------------

        for i in range(2, min(4, len(chars))):

            if chars[i] == "O":
                chars[i] = "0"

            elif chars[i] == "I":
                chars[i] = "1"

            elif chars[i] == "B":
                chars[i] = "8"

            elif chars[i] == "S":
                chars[i] = "5"

        # -----------------------
        # Step 4 : Series
        # Usually next 1-3 letters
        # -----------------------

        for i in range(4, min(7, len(chars))):

            if chars[i] == "0":
                chars[i] = "O"

            elif chars[i] == "1":
                chars[i] = "I"

            elif chars[i] == "8":
                chars[i] = "B"

        # -----------------------
        # Step 5 : Last Numbers
        # Remaining characters should be digits
        # -----------------------

        for i in range(7, len(chars)):

            if chars[i] == "O":
                chars[i] = "0"

            elif chars[i] == "I":
                chars[i] = "1"

            elif chars[i] == "B":
                chars[i] = "8"

            elif chars[i] == "S":
                chars[i] = "5"

            elif chars[i] == "Z":
                chars[i] = "2"

        corrected = "".join(chars)

        # -----------------------
        # Step 6 : Validate
        # -----------------------

        pattern = (
            r"[A-Z]{2}"
            r"[0-9]{1,2}"
            r"[A-Z]{1,3}"
            r"[0-9]{3,4}"
        )

        match = re.search(pattern, corrected)

        if match:

            vehicle_no = match.group()


            return vehicle_no


        return None