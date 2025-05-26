from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.social_media.social_media_dao import SocialMediaDAO
from base.utils.custom_exception import AppServices
from base.vo.social_media_vo import SocialMediaVO

logger = get_logger()


class SocialMediaService:
    @staticmethod
    def insert_social_media_service(social_media_dto):
        """
        Request:
            - social_media_dto: Data transfer object containing social media details including country_id, title, description, url, and status.

        Response:
            - On success: Returns HTTP 200 with inserted social media data.
            - On failure: Returns HTTP 400 or 404 with appropriate error message.

        Purpose:
            - To insert a new social media record associated with a valid country into the system.
            - Ensures that the referenced country exists before insertion.

        Company:
            Softvan Pvt Ltd
        """
        try:
            country_vo = CountryDAO.get_country_by_id_dao(
                social_media_dto.country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "try another country",
                    success=False,
                    data={},
                )

            social_media_vo = SocialMediaVO()
            social_media_vo.social_media_country_id = country_vo.country_id
            social_media_vo.social_media_country_name = country_vo.country_name
            social_media_vo.social_media_title = social_media_dto.social_media_title
            social_media_vo.social_media_description = (
                social_media_dto.social_media_description
            )
            social_media_vo.social_media_url = social_media_dto.social_media_url
            social_media_vo.social_media_status = social_media_dto.social_media_status

            social_media_insert_data = SocialMediaDAO.insert_social_media_dao(
                social_media_vo
            )

            if not social_media_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted social media: %s",
                        social_media_vo.social_media_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=social_media_insert_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_social_media_service(
            page_number, page_size, search_value, sort_by, sort_as
    ):
        """
        Request:
            - page_number: Integer indicating the page of results to return.
            - page_size: Number of records per page.
            - search_value: Optional string to filter results based on search criteria.
            - sort_by: Field name by which to sort results.
            - sort_as: Sort direction ('asc' or 'desc').

        Response:
            - On success: Returns HTTP 200 with paginated, sorted, and filtered social media records.
            - On failure: Returns HTTP 400 if no records found.

        Purpose:
            - To retrieve a paginated, searchable, and sortable list of all social media records.

        Company:
            Softvan Pvt Ltd
        """
        try:
            result = SocialMediaDAO.get_all_social_media_dao(
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
    def delete_social_media_service(social_media_id):
        """
        Request:
            - social_media_id: Integer or string representing the ID of the social media record to be deleted.

        Response:
            - On success: Returns HTTP 202 (Accepted) confirming the soft deletion.
            - On failure: Returns HTTP 400 if record not found.

        Purpose:
            - To perform a soft delete on a social media record by marking it as deleted without removing from database.

        Company:
            Softvan Pvt Ltd
        """
        try:
            delete_social_media_data = SocialMediaDAO.delete_social_media_dao(
                social_media_id
            )

            if not delete_social_media_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_social_media_data.is_deleted = True  # Soft delete

            logger.info("Deleted social media with ID: %s", social_media_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_social_media_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_social_media_by_id_service(social_media_id):
        """
        Request:
            - social_media_id: Identifier of the social media record to retrieve.

        Response:
            - On success: Returns HTTP 202 with social media details.
            - On failure: Returns HTTP 400 if record not found.

        Purpose:
            - To fetch detailed information about a specific social media entry by its ID.

        Company:
            Softvan Pvt Ltd
        """
        try:
            social_media_detail = SocialMediaDAO.get_social_media_by_id_dao(
                social_media_id
            )

            if not social_media_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched social_media detail for ID: %s",
                        social_media_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=social_media_detail,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_social_media_service(social_media_dto):
        """
        Request:
            - social_media_dto: DTO containing updated social media data including social_media_id.

        Response:
            - On success: Returns HTTP 202 with updated social media data.
            - On failure: Returns HTTP 400 if the social media or related country record does not exist or update fails.

        Purpose:
            - To update an existing social media record, validating the existence of referenced country and applying partial updates.

        Company:
            Softvan Pvt Ltd
        """
        try:
            existing_social_media = SocialMediaDAO.get_social_media_by_id_dao(
                social_media_dto.social_media_id
            )

            if not existing_social_media:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if social_media_dto.social_media_id is not None:
                existing_social_media.social_media_id = social_media_dto.social_media_id

            if social_media_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(
                    social_media_dto.country_id
                )
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_social_media.social_media_country_id = country_vo.country_id
                existing_social_media.social_media_country_name = (
                    country_vo.country_name
                )

            if social_media_dto.social_media_title is not None:
                existing_social_media.social_media_title = (
                    social_media_dto.social_media_title
                )

            if social_media_dto.social_media_description is not None:
                existing_social_media.social_media_description = (
                    social_media_dto.social_media_description
                )

            if social_media_dto.social_media_url is not None:
                existing_social_media.social_media_url = (
                    social_media_dto.social_media_url
                )

            if social_media_dto.social_media_status is not None:
                existing_social_media.social_media_status = (
                    social_media_dto.social_media_status
                )

            # Persist updated data
            updated_social_media = SocialMediaDAO.update_social_media_dao(
                existing_social_media
            )

            if not updated_social_media:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info(
                "Updated social media with ID: %s",
                social_media_dto.social_media_id
            )
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_social_media,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)
