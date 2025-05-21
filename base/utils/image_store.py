from base.config.logger_config import get_logger

logger = get_logger()

UPLOAD_DIR = "static/product_image/"


class ProductImageUploader:
    @staticmethod
    def save_image(images):
        """Save uploaded image(s) with original names and return their names and paths."""
        try:
            file_paths = []
            file_names = []

            if not isinstance(images, list):
                images = [images]

            if images:
                os.makedirs(UPLOAD_DIR, exist_ok=True)

                for image in images:
                    # Extract original filename without any FastAPI prefix
                    original_filename = os.path.basename(
                        image.filename
                    )  # 🔥 Ensures only the filename remains
                    image_path = os.path.join(UPLOAD_DIR, original_filename)

                    with open(image_path, "wb") as buffer:
                        buffer.write(
                            image.file.read())  # ✅ Fix from previous issue

                    file_paths.append(image_path)
                    file_names.append(
                        original_filename)  # ✅ Store only clean filename

                return file_names, file_paths

            return None, None

        except Exception as exception:
            logger.exception("Error saving image")
            return AppServices.handle_exception(exception, is_raise=True)


import os

from base.config.logger_config import get_logger
from base.utils.custom_exception import AppServices

logger = get_logger()

UPLOAD_DIR = "static/product_image/"


class ProductImageUploader:
    @staticmethod
    def save_image(images):
        """Save uploaded image(s) with original names and return their names and paths."""
        try:
            file_paths = []
            file_names = []

            if not isinstance(images, list):
                images = [images]

            if images:
                os.makedirs(UPLOAD_DIR, exist_ok=True)

                for image in images:
                    # Extract original filename without any FastAPI prefix
                    original_filename = os.path.basename(
                        image.filename
                    )  # 🔥 Ensures only the filename remains
                    image_path = os.path.join(UPLOAD_DIR, original_filename)

                    with open(image_path, "wb") as buffer:
                        buffer.write(
                            image.file.read())  # ✅ Fix from previous issue

                    file_paths.append(image_path)
                    file_names.append(
                        original_filename)  # ✅ Store only clean filename

                return file_names, file_paths

            return None, None

        except Exception as exception:
            logger.exception("Error saving image")
            return AppServices.handle_exception(exception, is_raise=True)
