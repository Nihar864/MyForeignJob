from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.news.news_dao import NewsDAO
from base.utils.custom_exception import AppServices
from base.vo.news_vo import NewsVO

logger = get_logger()


class NewsService:
    """
    Service layer handling all business logic related to news management.
    Company Name: Softvan Pvt Ltd
    """

    @staticmethod
    def insert_news_service(news_dto):
        """
        Purpose:
            Insert a new news record into the database.

        Request:
            news_dto (object): Data transfer object containing news details such as
                - country_id (int)
                - news_title (str)
                - news_description (str)
                - news_url (str)
                - news_status (str)

        Response:
            dict: Standardized response with status code, message, success flag, and data.

        Company Name:
            Softvan Pvt Ltd
        """
        try:
            country_vo = CountryDAO.get_country_by_id_dao(news_dto.country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "try another country",
                    success=False,
                    data={},
                )

            news_vo = NewsVO()
            news_vo.news_country_id = country_vo.country_id
            news_vo.news_country_name = country_vo.country_name
            news_vo.news_title = news_dto.news_title
            news_vo.news_description = news_dto.news_description
            news_vo.news_url = news_dto.news_url
            news_vo.news_status = news_dto.news_status

            news_insert_data = NewsDAO.insert_news_dao(news_vo)

            if not news_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted news: %s", news_vo.news_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=news_insert_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_news_service(page_number, page_size, search_value, sort_by, sort_as):
        """
        Purpose:
            Retrieve paginated, searchable, and sortable list of all news records.

        Request:
            page_number (int): Page number for pagination.
            page_size (int): Number of records per page.
            search_value (str): Search string to filter news records.
            sort_by (str): Field name to sort results.
            sort_as (str): Sort direction, e.g., 'asc' or 'desc'.

        Response:
            dict: Standardized response containing paginated list of news data.

        Company Name:
            Softvan Pvt Ltd
        """
        try:
            result = NewsDAO.get_all_news_dao(
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
    def delete_news_service(news_id):
        """
        Purpose:
            Soft delete a news record by its ID.

        Request:
            news_id (int): Unique identifier of the news to be deleted.

        Response:
            dict: Standardized response confirming deletion or failure.

        Company Name:
            Softvan Pvt Ltd
        """
        try:
            delete_news_data = NewsDAO.delete_news_dao(news_id)

            if not delete_news_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_news_data.is_deleted = True  # Soft delete flag

            logger.info("Deleted news with ID: %s", news_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_news_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_news_by_id_service(news_id):
        """
        Purpose:
            Retrieve detailed information for a news record by its ID.

        Request:
            news_id (int): Unique identifier of the news.

        Response:
            dict: Standardized response containing news details or error message.

        Company Name:
            Softvan Pvt Ltd
        """
        try:
            news_detail = NewsDAO.get_news_by_id_dao(news_id)

            if not news_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched news detail for ID: %s", news_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=news_detail,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_news_service(news_dto):
        """
        Purpose:
            Update an existing news record with new information.

        Request:
            news_dto (object): Data transfer object containing updated news details including
                - news_id (int)
                - country_id (int)
                - news_title (str)
                - news_description (str)
                - news_url (str)
                - news_status (str)

        Response:
            dict: Standardized response confirming update success or failure.

        Company Name:
            Softvan Pvt Ltd
        """
        try:
            existing_news = NewsDAO.get_news_by_id_dao(news_dto.news_id)

            if not existing_news:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if news_dto.news_id is not None:
                existing_news.news_id = news_dto.news_id

            if news_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(news_dto.country_id)
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_news.news_country_id = country_vo.country_id
                existing_news.news_country_name = country_vo.country_name

            if news_dto.news_title is not None:
                existing_news.news_title = news_dto.news_title

            if news_dto.news_description is not None:
                existing_news.news_description = news_dto.news_description

            if news_dto.news_url is not None:
                existing_news.news_url = news_dto.news_url

            if news_dto.news_status is not None:
                existing_news.news_status = news_dto.news_status

            updated_news = NewsDAO.update_news_dao(existing_news)

            if not updated_news:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated news with ID: %s", news_dto.news_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_news,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception, is_raise=True)
