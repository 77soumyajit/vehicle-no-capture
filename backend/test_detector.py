from ultralytics import YOLO

model = YOLO("weights/plate_detector.pt")

results = model.predict(
    source="uploads/vehicles/96803154-2d65-416e-9798-60cbd800c2ce.jpeg",
    imgsz=1280,
    conf=0.20,
    save=True,
    save_txt=True,
    save_conf=True,
    verbose=True,
)

print(results)