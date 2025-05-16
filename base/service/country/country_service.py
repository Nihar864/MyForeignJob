import shutil
from pathlib import Path

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dto.country.country_dto import GetAllCountryDTO
from base.utils.custom_exception import AppServices
from base.vo.country_vo import CountryVO

logger = get_logger()


class CountryService:

    @staticmethod
    def insert_country_service(
            country_name,
            country_description,
            show_on_homepage_status,
            country_status,
            country_currency,
            country_image,
            country_flag_image,
    ):
        """Convert form data to VO & Insert country, including both images."""

        try:
            # lowercountry_name = country_name.strip().lower()
            existing_country = CountryDAO.check_existing_user(
                country_name)
            if existing_country:
                return (
                    f"The country name '{country_name}' is already in use. Please choose a different name.",)

            # Directories for images
            country_image_dir = Path("static/country_image")
            flag_image_dir = Path("static/country_flag_image")

            country_image_dir.mkdir(parents=True, exist_ok=True)
            flag_image_dir.mkdir(parents=True, exist_ok=True)

            country_image_path = country_image_dir / country_image.filename
            with open(country_image_path, "wb") as buffer:
                shutil.copyfileobj(country_image.file, buffer)

            flag_image_path = flag_image_dir / country_flag_image.filename
            with open(flag_image_path, "wb") as buffer:
                shutil.copyfileobj(country_flag_image.file, buffer)

            # Prepare VO object
            country_vo = CountryVO()
            country_vo.country_name = country_name
            country_vo.country_description = country_description
            country_vo.country_image_names = country_image.filename
            country_vo.country_image_paths = str(country_image_path)
            country_vo.country_flag_image_name = country_flag_image.filename
            country_vo.country_flag_image_path = str(flag_image_path)
            country_vo.country_currency = country_currency
            country_vo.show_on_homepage_status = show_on_homepage_status
            country_vo.country_status = country_status

            # DAO call
            country_insert_data = CountryDAO.insert_country_dao(country_vo)

            if not country_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted country: %s", country_vo.country_name)
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
    def get_all_categories_service(dto: GetAllCountryDTO):
        try:
            get_all_data_result = CountryDAO.get_all_categories_dao(
                page_number=dto.page_number,
                page_size=dto.page_size,
                search_value=dto.search_value,
                sort_by=dto.sort_by,
                sort_as=dto.sort_as.value,
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
            country_id,
            country_name,
            country_description,
            show_on_homepage_status,
            country_currency,
            country_status,
            country_image,
            country_flag_image,
    ):
        try:
            existing_country = CountryDAO.get_country_by_id_dao(country_id)

            if not existing_country:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if country_name is not None:
                existing_country.country_name = country_name

            if country_description is not None:
                existing_country.country_description = country_description

            if show_on_homepage_status is not None:
                existing_country.show_on_homepage_status = show_on_homepage_status

            if country_currency is not None:
                existing_country.country_currency = country_currency

            if country_status is not None:
                existing_country.country_status = country_status

            allowed_extensions = {"png", "jpg", "jpeg", "gif"}

            if country_image is not None:
                extension = country_image.filename.split(".")[-1].lower()
                if extension not in allowed_extensions:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.BAD_REQUEST.value,
                        "Invalid country image format.",
                        success=False,
                        data={},
                    )

                upload_dir = Path("static/country_image")
                upload_dir.mkdir(parents=True, exist_ok=True)
                safe_filename = f"{country_image.filename}"
                file_path = upload_dir / safe_filename

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(country_image.file, buffer)

                existing_country.country_image_names = safe_filename
                existing_country.country_image_paths = str(file_path)

            if country_flag_image is not None:
                extension = country_flag_image.filename.split(".")[-1].lower()
                if extension not in allowed_extensions:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.BAD_REQUEST.value,
                        "Invalid country flag image format.",
                        success=False,
                        data={},
                    )

                flag_upload_dir = Path("static/country_flag_image")
                flag_upload_dir.mkdir(parents=True, exist_ok=True)
                safe_flag_filename = f"{country_flag_image.filename}"
                flag_file_path = flag_upload_dir / safe_flag_filename

                with open(flag_file_path, "wb") as buffer:
                    shutil.copyfileobj(country_flag_image.file, buffer)

                existing_country.country_flag_image_name = safe_flag_filename
                existing_country.country_flag_image_path = str(flag_file_path)

            updated_country_data = CountryDAO.update_country_dao(
                existing_country)

            if not updated_country_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated country with ID: %s", country_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_country_data,
            )

        except Exception as exception:
            logger.exception("Error updating country")
            return AppServices.handle_exception(exception)
