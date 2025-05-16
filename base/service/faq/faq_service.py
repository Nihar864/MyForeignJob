from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.faq.faq_dao import FaqDAO
from base.utils.custom_exception import AppServices
from base.vo.faq_vo import FaqVO

logger = get_logger()


class FaqService:

    @staticmethod
    def insert_faq_service(faq_dto):

        try:
            country_vo = CountryDAO.get_country_by_id_dao(faq_dto.country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "this country is not exist",
                    success=False,
                    data={},
                )

            faq_vo = FaqVO()
            faq_vo.faq_country_id = country_vo.country_id
            faq_vo.faq_country_name = country_vo.country_name
            faq_vo.faq_title = faq_dto.faq_title
            faq_vo.faq_description = faq_dto.faq_description

            faq_insert_data = FaqDAO.insert_faq_dao(faq_vo)

            if not faq_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted faq: %s", faq_vo.faq_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=faq_insert_data,
            )

        except Exception as exception:
            logger.exception("Error inserting faq")
            return AppServices.handle_exception(exception,is_raise=True)

    @staticmethod
    def get_all_faq_service(page_number, page_size, search_value, sort_by,
                            sort_as):
        try:
            result = FaqDAO.get_all_faq_dao(
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
            logger.exception("Error fetching all faq")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_faq_service(faq_id):
        """Soft delete a faq by ID."""
        try:
            delete_faq_data = FaqDAO.delete_faq_dao(faq_id)

            if not delete_faq_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_faq_data.is_deleted = True  # Soft delete

            logger.info("Deleted faq with ID: %s", faq_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_faq_data,
            )

        except Exception as exception:
            logger.exception("Error deleting faq with ID: %s", faq_id)
            return AppServices.handle_exception(exception,is_raise=True)

    @staticmethod
    def get_faq_by_id_service(faq_id):
        """Retrieve faq details for a given ID."""
        try:
            faq_detail = FaqDAO.get_faq_by_id_dao(faq_id)

            if not faq_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched faq detail for ID: %s", faq_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=faq_detail,
            )

        except Exception as exception:
            logger.exception("Error retrieving faq with ID: %s", faq_id)
            return AppServices.handle_exception(exception,is_raise=True)

    @staticmethod
    def update_faq_service(faq_dto):
        try:
            existing_faq = FaqDAO.get_faq_by_id_dao(faq_dto.faq_id)

            if not existing_faq:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if faq_dto.faq_id is not None:
                existing_faq.faq_id = faq_dto.faq_id

            if faq_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(
                    faq_dto.country_id)
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_faq.faq_country_id = country_vo.country_id
                existing_faq.faq_country_name = country_vo.country_name

            if faq_dto.faq_title is not None:
                existing_faq.faq_title = faq_dto.faq_title

            if faq_dto.faq_description is not None:
                existing_faq.faq_description = faq_dto.faq_description

            # Step 3: Persist updated data
            updated_faq = FaqDAO.update_faq_dao(existing_faq)

            if not updated_faq:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated faq with ID: %s", faq_dto.faq_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_faq,
            )

        except Exception as exception:
            logger.exception("Error updating faq")
            return AppServices.handle_exception(exception,is_raise=True)