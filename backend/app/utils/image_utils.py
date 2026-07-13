from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads/vehicles")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_uploaded_image(file: UploadFile):

    extension = file.filename.split(".")[-1]

    stored_name = f"{uuid4()}.{extension}"

    filepath = UPLOAD_DIR / stored_name

    with open(filepath, "wb") as image:

        image.write(file.file.read())

    return {
        "original_name": file.filename,
        "stored_name": stored_name,
        "image_path": str(filepath),
    }