from fastapi import APIRouter, Response, Query, Request

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.news.news_dto import NewsDTO, UpdateNewsDTO
from base.service.login.login_service import login_required
from base.service.news.news_service import NewsService
from base.utils.custom_exception import AppServices

logger = get_logger()

news_router = APIRouter(
    prefix="/news",
    tags=["News"],
    responses={},
)


@news_router.post("/add")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_news_controller(
        request: Request,
        news_dto: NewsDTO,
        response: Response,
):
    try:
        if not news_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False, )

        response_payload = NewsService.insert_news_service(news_dto)

        logger.info(f"social media inserted: {response_payload}")
        return response_payload

    except Exception as exception:
        logger.error(f"Error in insert_news_controller: {exception}")
        return AppServices.handle_exception(exception, is_raise=True)


@news_router.get("/all")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_news_controller(
        request: Request,
        page_number: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        search_value: str = "",
        sort_by: str = "news_title",
        sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING)
):
    return NewsService.get_all_news_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@news_router.delete("/{news_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_news_controller(request: Request, news_id):
    try:
        response_payload = NewsService.delete_news_service(news_id)
        logger.info(f"Deleted social media with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting social media")
        return AppServices.handle_exception(exception, is_raise=True)


@news_router.get("/{news_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_news_by_id_controller(request: Request, news_id: int):
    try:
        logger.info(f"Fetching social media details for ID: {news_id}")
        response_payload = NewsService.get_news_by_id_service(news_id)
        logger.info(f"Fetched social media details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching social media details")
        return AppServices.handle_exception(exception, is_raise=True)


@news_router.put("/update")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_news_controller(request: Request,
                           news_dto: UpdateNewsDTO,
                           ):
    try:
        response_payload = NewsService.update_news_service(news_dto)
        logger.info(f"Updated news with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating news")
        return AppServices.handle_exception(exception, is_raise=True)
