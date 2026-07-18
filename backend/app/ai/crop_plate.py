import os
import cv2


class PlateCropper:

    @staticmethod
    def crop(image_path, results):

        image = cv2.imread(image_path)

        if image is None:
            return None

        height, width = image.shape[:2]

        best_box = None
        best_conf = 0

        for result in results:

            for box in result.boxes:

                conf = float(box.conf[0])

                if conf > best_conf:
                    best_conf = conf
                    best_box = box

        if best_box is None:
            return None

        x1, y1, x2, y2 = map(int, best_box.xyxy[0])

        pad_x = int((x2 - x1) * 0.10)
        pad_y = int((y2 - y1) * 0.10)

        x1 = max(0, x1 - pad_x)
        y1 = max(0, y1 - pad_y)

        x2 = min(width, x2 + pad_x)
        y2 = min(height, y2 + pad_y)

        crop = image[y1:y2, x1:x2]

        os.makedirs("cropped", exist_ok=True)

        output = os.path.join(
            "cropped",
            "plate.jpg",
        )

        cv2.imwrite(output, crop)

        return output