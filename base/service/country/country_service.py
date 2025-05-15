import shutil
from pathlib import Path

from django.template.defaultfilters import lower

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.utils.custom_exception import AppServices
from base.vo.country_vo import CountryVO

logger = get_logger()


class CountryService:

    @staticmethod
    def insert_country_service(
            countryName,
            countryDescription,
            showOnHomepageStatus,
            countryStatus,
            countryCurrency,
            countryImage,
            countryFlagImage,
    ):
        """Convert form data to VO & Insert country, including both images."""

        try:
            # lowerCountryName = countryName.strip().lower()
            existing_country = CountryDAO.check_existing_user(
                countryName)
            if existing_country:
                return (f"The country name '{countryName}' is already in use. Please choose a different name.",)

            # Directories for images
            country_image_dir = Path("static/country_image")
            flag_image_dir = Path("static/country_flag_image")

            country_image_dir.mkdir(parents=True, exist_ok=True)
            flag_image_dir.mkdir(parents=True, exist_ok=True)

            country_image_path = country_image_dir / countryImage.filename
            with open(country_image_path, "wb") as buffer:
                shutil.copyfileobj(countryImage.file, buffer)

            flag_image_path = flag_image_dir / countryFlagImage.filename
            with open(flag_image_path, "wb") as buffer:
                shutil.copyfileobj(countryFlagImage.file, buffer)

            # Prepare VO object
            country_vo = CountryVO()
            country_vo.countryName = countryName
            country_vo.countryDescription = countryDescription
            country_vo.countryImageNames = countryImage.filename
            country_vo.countryImagePaths = str(country_image_path)
            country_vo.countryFlagImageName = countryFlagImage.filename
            country_vo.countryFlagImagePath = str(flag_image_path)
            country_vo.countryCurrency = countryCurrency
            country_vo.showOnHomepageStatus = showOnHomepageStatus
            country_vo.countryStatus = countryStatus

            # DAO call
            country_insert_data = CountryDAO.insert_country_dao(country_vo)

            if not country_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted country: %s", country_vo.countryName)
            return AppServices.app_response(
                HttpStatusCodeEnum.CREATED.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=country_insert_data,
            )

        except Exception as exception:
            logger.exception("Error inserting country")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_categories_service(pageNumber, pageSize, searchValue, sortBy,
                                   sortAs):
        try:
            get_all_data_result = CountryDAO.get_all_categories_dao(
                pageNumber=pageNumber,
                pageSize=pageSize,
                searchValue=searchValue,
                sortBy=sortBy,
                sortAs=sortAs,
            )

            if not get_all_data_result["items"]:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=get_all_data_result,
            )

        except Exception as exception:
            logger.exception("Error fetching all countries")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_country_service(countryId):
        """Soft delete a country by ID."""
        try:
            delete_country_data = CountryDAO.delete_country_dao(countryId)

            if not delete_country_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_country_data.is_deleted = True  # Soft delete

            logger.info("Deleted country with ID: %s", countryId)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_country_data,
            )

        except Exception as exception:
            logger.exception("Error deleting country with ID: %s", countryId)
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_country_by_id_service(countryId):
        """Retrieve country details for a given ID."""
        try:
            country_detail_from_id = CountryDAO.get_country_by_id_dao(
                countryId)

            if not country_detail_from_id:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched country detail for ID: %s", countryId)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=country_detail_from_id,
            )

        except Exception as exception:
            logger.exception("Error retrieving country with ID: %s", countryId)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_country_service(
            countryId,
            countryName,
            countryDescription,
            showOnHomepageStatus,
            countryCurrency,
            countryStatus,
            countryImage,
            countryFlagImage,
    ):
        try:
            existing_country = CountryDAO.get_country_by_id_dao(countryId)

            if not existing_country:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if countryName is not None:
                existing_country.countryName = countryName

            if countryDescription is not None:
                existing_country.countryDescription = countryDescription

            if showOnHomepageStatus is not None:
                existing_country.showOnHomepageStatus = showOnHomepageStatus

            if countryCurrency is not None:
                existing_country.countryCurrency = countryCurrency

            if countryStatus is not None:
                existing_country.countryStatus = countryStatus

            allowed_extensions = {"png", "jpg", "jpeg", "gif"}

            if countryImage is not None:
                extension = countryImage.filename.split(".")[-1].lower()
                if extension not in allowed_extensions:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.BAD_REQUEST.value,
                        "Invalid country image format.",
                        success=False,
                        data={},
                    )

                upload_dir = Path("static/country_image")
                upload_dir.mkdir(parents=True, exist_ok=True)
                safe_filename = f"{countryImage.filename}"
                file_path = upload_dir / safe_filename

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(countryImage.file, buffer)

                existing_country.countryImageNames = safe_filename
                existing_country.countryImagePaths = str(file_path)

            if countryFlagImage is not None:
                extension = countryFlagImage.filename.split(".")[-1].lower()
                if extension not in allowed_extensions:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.BAD_REQUEST.value,
                        "Invalid country flag image format.",
                        success=False,
                        data={},
                    )

                flag_upload_dir = Path("static/country_flag_image")
                flag_upload_dir.mkdir(parents=True, exist_ok=True)
                safe_flag_filename = f"{countryFlagImage.filename}"
                flag_file_path = flag_upload_dir / safe_flag_filename

                with open(flag_file_path, "wb") as buffer:
                    shutil.copyfileobj(countryFlagImage.file, buffer)

                existing_country.countryFlagImageName = safe_flag_filename
                existing_country.countryFlagImagePath = str(flag_file_path)

            updated_country_data = CountryDAO.update_country_dao(
                existing_country)

            if not updated_country_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated country with ID: %s", countryId)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_country_data,
            )

        except Exception as exception:
            logger.exception("Error updating country")
            return AppServices.handle_exception(exception)
