from app.ai.plate_reader import PlateReader

result = PlateReader.read(
    "cropped/plate.jpg"
)

print(result)