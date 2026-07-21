import os
import cv2
import numpy as np


class ImageVariants:

    @staticmethod
    def generate(image_path):

        image = cv2.imread(image_path)

        if image is None:
            return [image_path]

        os.makedirs("cropped", exist_ok=True)

        paths = []

        def save(name, img):
            path = f"cropped/{name}.jpg"
            cv2.imwrite(path, img)
            paths.append(path)

        save("variant_original", image)

        upscaled = cv2.resize(
            image,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC,
        )

        save("variant_upscale", upscaled)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        save("variant_gray", gray)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )

        clahe_img = clahe.apply(gray)

        save("variant_clahe", clahe_img)

        bilateral = cv2.bilateralFilter(
            clahe_img,
            9,
            75,
            75,
        )

        save("variant_bilateral", bilateral)

        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0],
            ],
            dtype=np.float32,
        )

        sharpen = cv2.filter2D(
            bilateral,
            -1,
            kernel,
        )

        save("variant_sharpen", sharpen)

        adaptive = cv2.adaptiveThreshold(
            sharpen,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21,
            10,
        )

        save("variant_adaptive", adaptive)

        _, otsu = cv2.threshold(
            sharpen,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        save("variant_otsu", otsu)

        contrast = cv2.convertScaleAbs(
            gray,
            alpha=1.6,
            beta=10,
        )

        save("variant_contrast", contrast)

        morph_kernel = np.ones((2, 2), np.uint8)

        morph = cv2.morphologyEx(
            adaptive,
            cv2.MORPH_CLOSE,
            morph_kernel,
        )

        save("variant_morph", morph)

        return paths