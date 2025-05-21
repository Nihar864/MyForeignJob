from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.news.news_dao import NewsDAO
from base.utils.custom_exception import AppServices
from base.vo.news_vo import NewsVO

logger = get_logger()


class NewsService:

    @staticmethod
    def insert_news_service(news_dto):

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

            logger.info("Inserted news: %s",
                        news_vo.news_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=news_insert_data,
            )

        except Exception as exception:
            logger.exception("Error inserting news")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_all_news_service(page_number, page_size, search_value, sort_by,
                             sort_as):
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
            logger.exception("Error fetching all news")
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def delete_news_service(news_id):
        """Soft delete a news by ID."""
        try:
            delete_news_data = NewsDAO.delete_news_dao(news_id)

            if not delete_news_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_news_data.is_deleted = True  # Soft delete

            logger.info("Deleted news with ID: %s", news_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_news_data,
            )

        except Exception as exception:
            logger.exception("Error deleting news with ID: %s",
                             news_id)
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_news_by_id_service(news_id):
        """Retrieve news details for a given ID."""
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
            logger.exception("Error retrieving news with ID: %s",
                             news_id)
            return AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_news_service(news_dto):
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
                country_vo = CountryDAO.get_country_by_id_dao(
                    news_dto.country_id)
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

            # Step 3: Persist updated data
            updated_news = NewsDAO.update_news_dao(existing_news)

            if not updated_news:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated news with ID: %s",
                        news_dto.news_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_news,
            )

        except Exception as exception:
            logger.exception("Error updating news")
            return AppServices.handle_exception(exception, is_raise=True)
