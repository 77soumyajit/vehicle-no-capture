from ultralytics import YOLO

model = YOLO("weights/license_plate.pt")

print(model.names)