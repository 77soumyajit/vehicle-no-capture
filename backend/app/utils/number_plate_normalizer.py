class NumberPlateNormalizer:

    @staticmethod
    def normalize(text):

        if text is None:
            return None

        return (
            text.upper()
            .replace(" ", "")
            .replace("-", "")
            .replace(".", "")
        )