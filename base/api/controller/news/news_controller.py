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
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_news_controller(
    request: Request,
    news_dto: NewsDTO,
    response: Response,
):
    """
    Request:
        - news_dto (NewsDTO): Contains news title, description, author, publish date, etc.

    Response:
        - JSON: Returns confirmation and stored news ID if successfully inserted.

    Purpose:
        - To allow an admin to insert a new news item into the system.

    Company Name: Softvan Pvt Ltd
    """
    try:
        if not news_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )

        response_payload = NewsService.insert_news_service(news_dto)

        logger.info(f"social media inserted: {response_payload}")
        return response_payload

    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@news_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_news_controller(
    request: Request,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "news_title",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Request:
        - Query Params: page_number, page_size, search_value (optional), sort_by, sort_as.

    Response:
        - JSON: Paginated list of all news items with metadata and optional filters.

    Purpose:
        - To retrieve all news items for admin review with support for search, sort, and pagination.

    Company Name: Softvan Pvt Ltd
    """
    return NewsService.get_all_news_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@news_router.delete("/{news-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_news_controller(response: Response, request: Request, news_id):
    """
    Request:
        - Path Parameter: news_id (int) — ID of the news item to delete.

    Response:
        - JSON: Success or failure message with status.

    Purpose:
        - To delete a news item from the database by its ID.

    Company Name: Softvan Pvt Ltd
    """
    try:
        response_payload = NewsService.delete_news_service(news_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Deleted social media with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@news_router.get("/{news-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_news_by_id_controller(response: Response, request: Request, news_id: int):
    """
    Request:
        - Path Parameter: news_id (int) — ID of the news item to retrieve.

    Response:
        - JSON: Detailed information of the requested news item.

    Purpose:
        - To fetch and display a specific news item's complete details.

    Company Name: Softvan Pvt Ltd
    """
    try:
        logger.info(f"Fetching social media details for ID: {news_id}")
        response_payload = NewsService.get_news_by_id_service(news_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Fetched social media details: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@news_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_news_controller(
    response: Response,
    request: Request,
    news_dto: UpdateNewsDTO,
):
    """
    Request:
        - news_dto (UpdateNewsDTO): Contains news ID and updated fields such as title, content, etc.

    Response:
        - JSON: Success or failure message along with updated record info.

    Purpose:
        - To update an existing news record based on provided details.

    Company Name: Softvan Pvt Ltd
    """
    try:
        response_payload = NewsService.update_news_service(news_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated news with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)
