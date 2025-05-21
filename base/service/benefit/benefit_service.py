from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.benefit.benefit_dao import BenefitDAO
from base.dao.country.country_dao import CountryDAO
from base.utils.custom_exception import AppServices
from base.vo.benefit_vo import BenefitVO

logger = get_logger()


class BenefitService:

    # @staticmethod
    # def insert_benefit_service(country_id, benefit_title, benefit_description,
    #                            benefit_image):

    @staticmethod
    def insert_benefit_service(country_id, benefit_title,
                               benefit_description):

        try:
            existing_benefit = BenefitDAO.check_existing_benefit(benefit_title)
            if existing_benefit:
                return (
                    f"The Benefit Title '{benefit_title}' is already in use. "
                    f"Please choose a different Title.")

            country_vo = CountryDAO.get_country_by_id_dao(country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "try another country",
                    success=False,
                    data={})

            # # Directories for images
            # benefit_image_dir = Path("static/benefit_image")
            # benefit_image_dir.mkdir(parents=True, exist_ok=True)
            # benefit_image_path = benefit_image_dir / benefit_image.filename
            # with open(benefit_image_path, "wb") as buffer:
            #     shutil.copyfileobj(benefit_image.file, buffer)

            benefit_vo = BenefitVO()
            benefit_vo.benefit_country_id = country_vo.country_id
            benefit_vo.benefit_country_name = country_vo.country_name
            benefit_vo.benefit_title = benefit_title
            benefit_vo.benefit_description = benefit_description
            # benefit_vo.benefit_image_name = benefit_image.filename
            # benefit_vo.benefit_image_path = str(benefit_image_path)

            benefit_insert_data = BenefitDAO.insert_benefit_dao(benefit_vo)

            if not benefit_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted benefit: %s", benefit_vo.benefit_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=benefit_insert_data,
            )

        except Exception as exception:
            logger.exception("Error inserting benefit")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_benefit_service(page_number, page_size, search_value, sort_by,
                                sort_as):
        try:
            result = BenefitDAO.get_all_benefit_dao(
                page_number=page_number,
                page_size=page_size,
                search_value=search_value,
                sort_by=sort_by,
                sort_as=sort_as,
            )

            if not result["items"]:
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
                data=result,
            )

        except Exception as exception:
            logger.exception("Error fetching all benefit")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_benefit_service(benefit_id):
        """Soft delete a benefit by ID."""
        try:
            delete_benefit_data = BenefitDAO.delete_benefit_dao(benefit_id)

            if not delete_benefit_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_benefit_data.is_deleted = True  # Soft delete

            logger.info("Deleted benefit with ID: %s", benefit_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_benefit_data,
            )

        except Exception as exception:
            logger.exception("Error deleting benefit with ID: %s", benefit_id)
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_benefit_by_id_service(benefit_id):
        """Retrieve benefit details for a given ID."""
        try:
            benefit_detail = BenefitDAO.get_benefit_by_id_dao(benefit_id)

            if not benefit_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched benefit detail for ID: %s", benefit_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=benefit_detail,
            )

        except Exception as exception:
            logger.exception("Error retrieving benefit with ID: %s",
                             benefit_id)
            return AppServices.handle_exception(exception, is_raise=True)

    # @staticmethod
    # def update_benefit_service(benefit_id, country_id, benefit_title,
    #                            benefit_description, benefit_image):
    @staticmethod
    def update_benefit_service(benefit_id, country_id, benefit_title,
                               benefit_description):
        try:
            # First fetch the actual benefit to be updated by ID
            existing_benefit = BenefitDAO.get_benefit_by_id_dao(benefit_id)
            if not existing_benefit:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "Benefit not found for the given ID.",
                    success=False,
                    data={},
                )

            # Now check if the new title is already used by another benefit
            title_conflict = BenefitDAO.check_existing_benefit(benefit_title)
            if title_conflict and title_conflict.benefit_id != benefit_id:
                return (
                    f"The Benefit Title '{benefit_title}' is already in use. "
                    f"Please choose a different Title.")

            # Process country
            if country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(country_id)
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_benefit.benefit_country_id = country_vo.country_id
                existing_benefit.benefit_country_name = country_vo.country_name

            if benefit_title is not None:
                existing_benefit.benefit_title = benefit_title

            if benefit_description is not None:
                existing_benefit.benefit_description = benefit_description

            # allowed_extensions = {"png", "jpg", "jpeg", "gif"}
            #
            # if benefit_image is not None:
            #     extension = benefit_image.filename.split(".")[-1].lower()
            #     if extension not in allowed_extensions:
            #         return AppServices.app_response(
            #             HttpStatusCodeEnum.BAD_REQUEST.value,
            #             "Invalid benefit image format.",
            #             success=False,
            #             data={},
            #         )
            #
            #     upload_dir = Path("static/benefit_image")
            #     upload_dir.mkdir(parents=True, exist_ok=True)
            #     safe_filename = f"{benefit_image.filename}"
            #     file_path = upload_dir / safe_filename
            #
            #     with open(file_path, "wb") as buffer:
            #         shutil.copyfileobj(benefit_image.file, buffer)
            #
            #     existing_benefit.benefit_image_name = safe_filename
            #     existing_benefit.benefit_image_path = str(file_path)

            updated_benefit = BenefitDAO.update_benefit_dao(existing_benefit)

            if not updated_benefit:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated benefit with ID: %s", benefit_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_benefit,
            )

        except Exception as exception:
            logger.exception("Error updating benefit")
            return AppServices.handle_exception(exception, is_raise=True)
