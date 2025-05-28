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
    def insert_benefit_service(country_id, benefit_title, benefit_description):
        """
        Insert a new benefit into the system.

        Request:
            country_id (int): ID of the country associated with the benefit
            benefit_title (str): Title of the benefit
            benefit_description (str): Description of the benefit
            # benefit_image (UploadFile): Image file for the benefit (currently commented out)

        Response:
            dict: Response containing success status, message, and data

        Purpose:
            - Validates input parameters
            - Checks for existing benefits with same title
            - Creates new benefit record in database

        Company Name:
            - Softvan Pvt Ltd
        """
        try:
            existing_benefit = BenefitDAO.check_existing_benefit(benefit_title)
            if existing_benefit:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    f"The Benefit Title '{benefit_title}' is already in use. "
                    f"Please choose a different Title.",
                    success=False,
                    data={},
                )

            country_vo = CountryDAO.get_country_by_id_dao(country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "try another country",
                    success=False,
                    data={},
                )

            benefit_vo = BenefitVO()
            benefit_vo.benefit_country_id = country_vo.country_id
            benefit_vo.benefit_country_name = country_vo.country_name
            benefit_vo.benefit_title = benefit_title
            benefit_vo.benefit_description = benefit_description

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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_benefit_service(page_number, page_size, search_value, sort_by, sort_as):
        """
        Retrieve all benefits with pagination and filtering options.

        Request:
            page_number (int): Page number for pagination
            page_size (int): Number of items per page
            search_value (str): Value to search in benefit titles/descriptions
            sort_by (str): Field to sort by
            sort_as (SortingOrderEnum): Sorting order (ASC/DESC)

        Response:
            dict: Response containing paginated benefit data

        Purpose:
            - Provides paginated list of benefits
            - Supports searching and sorting
            - Response empty list if no benefits found

        Company Name:
            - Softvan Pvt Ltd
        """
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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_benefit_service(benefit_id):
        """
        Soft delete a benefit by its ID.

        Request:
            benefit_id (int): ID of the benefit to be deleted

        Response:
            dict: Response containing success status and message

        Purpose:
            - Marks benefit as deleted (soft delete)
            - Response error if benefit not found
            - Logs deletion activity

        Company Name:
            - Softvan Pvt Ltd
        """
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
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_benefit_by_id_service(benefit_id):
        """
        Retrieve detailed information about a specific benefit.

        Request:
            benefit_id (int): ID of the benefit to retrieve

        Response:
            dict: Response containing benefit details

        Purpose:
            - Fetches complete details of a single benefit
            - Response error if benefit not found
            - Useful for viewing/editing specific benefits

        Company Name:
            - Softvan Pvt Ltd
        """
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
            return AppServices.handle_exception(exception, is_raise=True)

    # @staticmethod
    # def update_benefit_service(benefit_id, country_id, benefit_title,
    #                            benefit_description, benefit_image):
    @staticmethod
    def update_benefit_service(
        benefit_id, country_id, benefit_title, benefit_description
    ):
        """
        Update an existing benefit's information.

        Request:
            benefit_id (int): ID of the benefit to update
            country_id (Optional[int]): New country ID if updating
            benefit_title (Optional[str]): New title if updating
            benefit_description (Optional[str]): New description if updating
            # benefit_image (Optional[UploadFile]): New image if updating (currently commented out)

        Response:
            dict: Response containing updated benefit data

        Purpose:
            - Allows partial or complete updates to benefit information
            - Validates new title uniqueness
            - Updates country reference if changed
            - Response updated benefit data

        Company Name:
            - Softvan Pvt Ltd
        """
        try:
            existing_benefit = BenefitDAO.check_existing_benefit(benefit_title)
            if existing_benefit:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    f"The Benefit Title '{benefit_title}' is already in use. "
                    f"Please choose a different Title.",
                    success=False,
                    data={},
                )

            title_conflict = BenefitDAO.check_existing_benefit(benefit_title)
            if title_conflict and title_conflict.benefit_id != benefit_id:
                return (
                    f"The Benefit Title '{benefit_title}' is already in use. "
                    f"Please choose a different Title."
                )

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
            return AppServices.handle_exception(exception, is_raise=True)
