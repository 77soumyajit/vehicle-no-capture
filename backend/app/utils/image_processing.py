import cv2


def preprocess_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return image_path

    # --------------------------------
    # Resize Image
    # --------------------------------

    image = cv2.resize(
        image,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # --------------------------------
    # Convert to Gray
    # --------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------
    # Noise Reduction
    # --------------------------------

    gray = cv2.bilateralFilter(
        gray,
        11,
        17,
        17
    )

    # --------------------------------
    # Adaptive Threshold
    # --------------------------------

    processed = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY,

        31,

        2,

    )

    processed_path = image_path.replace(
        ".",
        "_processed."
    )

    cv2.imwrite(
        processed_path,
        processed
    )

    return processed_path