from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.faq.faq_dao import FaqDAO
from base.utils.custom_exception import AppServices
from base.vo.faq_vo import FaqVO

logger = get_logger()


class FaqService:
    """
    Service class for managing FAQ operations including CRUD functionalities.

    Purpose:
        To provide a robust business logic layer that handles FAQ data manipulation,
        validation, and interaction with the persistence layer.

    Company Name:
        Softvan Pvt Ltd

    """

    @staticmethod
    def insert_faq_service(faq_dto):
        """
        Insert a new FAQ entry.


        Request:
            faq_dto (object): DTO containing the FAQ data to be inserted.
                - country_id: int
                - faq_title: str
                - faq_description: str

        Response:
            dict: Standardized response dictionary containing:
                - HTTP status code
                - Response message
                - Success flag (bool)
                - Data payload (inserted FAQ object or empty dict)

        Purpose:
            To add a new FAQ record associated with a valid country, ensuring data integrity
            and returning an appropriate standardized response.

        Company Name:
            Softvan Pvt Ltd
        """
        try:
            country_vo = CountryDAO.get_country_by_id_dao(faq_dto.country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "try another country",
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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_faq_service(page_number, page_size, search_value, sort_by, sort_as):
        """
        Retrieve all FAQs with pagination, searching, and sorting.


        Request:
            page_number (int): Current page number.
            page_size (int): Number of FAQs per page.
            search_value (str): Search keyword to filter FAQs.
            sort_by (str): Field name to sort the FAQs.
            sort_as (str): Sort order direction ('asc' or 'desc').

        Response:
            dict: Standardized response including:
                - HTTP status code
                - Message
                - Success flag
                - Data containing paginated FAQ items or empty dict if none found.

        Purpose:
            To fetch FAQs in a paginated manner with optional search and sorting,
            facilitating efficient data retrieval for client applications.

        Company Name:
            Softvan Pvt Ltd
        """
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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_faq_service(faq_id):
        """
        Perform a soft delete on a FAQ by its ID.


        Request:
            faq_id (int): Unique identifier of the FAQ to be soft deleted.

        Response:
            dict: Response indicating success or failure with:
                - HTTP status code
                - Message
                - Success flag
                - Data containing the updated FAQ object marked as deleted.

        Purpose:
            To mark a FAQ record as deleted without physical removal,
            maintaining historical integrity of the data.

        Company Name:
            Softvan Pvt Ltd
        """
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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_faq_by_id_service(faq_id):
        """
        Retrieve detailed FAQ information by ID.

        Request:
            faq_id (int): Identifier of the FAQ to retrieve.

        Response:
            dict: Response with:
                - HTTP status code
                - Message
                - Success flag
                - Data containing the FAQ details or empty dict if not found.

        Purpose:
            To fetch the full FAQ details for a given FAQ ID,
            ensuring the record exists before returning.

        Company Name:
            Softvan Pvt Ltd
        """
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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_faq_service(faq_dto):
        """
        Update an existing FAQ entry.

        Request:
            faq_dto (object): DTO with FAQ update information including:
                - faq_id: int (mandatory for update)
                - country_id: int (optional)
                - faq_title: str (optional)
                - faq_description: str (optional)

        Response:
            dict: Structured response with:
                - HTTP status code
                - Message
                - Success flag
                - Data containing updated FAQ object or empty dict on failure.

        Purpose:
            To modify the details of an existing FAQ,
            validating referenced country and persisting updates.

        Company Name:
            Softvan Pvt Ltd
        """
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
                country_vo = CountryDAO.get_country_by_id_dao(faq_dto.country_id)
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

            # Persist updated data
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
            return AppServices.handle_exception(exception, is_raise=True)
