from pathlib import Path

from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "weights" / "plate_detector.pt"

model = YOLO(str(MODEL_PATH))


class PlateDetector:

    @staticmethod
    def detect(image_path):

        return model.predict(
            source=str(image_path),
            conf=0.25,
            imgsz=640,
            save=False,
            verbose=False,
        )