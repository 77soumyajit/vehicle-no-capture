import cv2
import os


class ImageVariants:

    @staticmethod
    def generate(image_path):

        image = cv2.imread(image_path)

        if image is None:
            return [image_path]

        os.makedirs("cropped", exist_ok=True)

        paths = []

        # -------------------------
        # Original
        # -------------------------

        original = "cropped/variant_original.jpg"

        cv2.imwrite(
            original,
            image
        )

        paths.append(original)

        # -------------------------
        # Upscale 2x
        # -------------------------

        upscaled = cv2.resize(

            image,

            None,

            fx=2,

            fy=2,

            interpolation=cv2.INTER_CUBIC

        )

        upscale_path = "cropped/variant_upscale.jpg"

        cv2.imwrite(
            upscale_path,
            upscaled
        )

        paths.append(upscale_path)

        # -------------------------
        # Gray
        # -------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray_path = "cropped/variant_gray.jpg"

        cv2.imwrite(
            gray_path,
            gray
        )

        paths.append(gray_path)

        # -------------------------
        # Adaptive Threshold
        # -------------------------

        thresh = cv2.adaptiveThreshold(

            gray,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY,

            21,

            10

        )

        thresh_path = "cropped/variant_threshold.jpg"

        cv2.imwrite(
            thresh_path,
            thresh
        )

        paths.append(thresh_path)

        # -------------------------
        # Bilateral Filter
        # -------------------------

        smooth = cv2.bilateralFilter(

            gray,

            9,

            75,

            75

        )

        smooth_path = "cropped/variant_bilateral.jpg"

        cv2.imwrite(
            smooth_path,
            smooth
        )

        paths.append(smooth_path)

        return paths