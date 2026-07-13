from app.models.uploaded_image import UploadedImage
from app.repositories.upload_repository import UploadRepository
from app.utils.image_utils import save_uploaded_image


class UploadService:

    @staticmethod
    def upload_image(db, file):

        image = save_uploaded_image(file)

        uploaded = UploadedImage(

            original_name=image["original_name"],

            stored_name=image["stored_name"],

            image_path=image["image_path"]

        )

        return UploadRepository.create(
            db,
            uploaded
        )