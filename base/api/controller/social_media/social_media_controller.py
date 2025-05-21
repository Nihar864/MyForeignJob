from fastapi import APIRouter, Response, Query, Request

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.social_media.social_media_dto import UpdateSocialMediaDTO, \
    SocialMediaDTO
from base.service.login.login_service import login_required
from base.service.social_media.social_media_service import SocialMediaService
from base.utils.custom_exception import AppServices

logger = get_logger()

social_media_router = APIRouter(
    prefix="/social_media",
    tags=["SocialMedia"],
    responses={},
)


@social_media_router.post("/add")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_social_media_controller(request: Request,
                                   social_media_dto: SocialMediaDTO,
                                   response: Response,
                                   ):
    try:
        if not social_media_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False, )

        response_payload = SocialMediaService.insert_social_media_service(
            social_media_dto)

        logger.info(f"social media inserted: {response_payload}")
        return response_payload

    except Exception as exception:
        logger.error(f"Error in insert_social_media_controller: {exception}")
        return AppServices.handle_exception(exception, is_raise=True)


@social_media_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_social_media_controller(request: Request,
                                 page_number: int = Query(1, ge=1),
                                 page_size: int = Query(10, ge=1),
                                 search_value: str = "",
                                 sort_by: str = "social_media_title",
                                 sort_as: SortingOrderEnum = Query(
                                     SortingOrderEnum.ASCENDING)
                                 ):
    return SocialMediaService.get_all_social_media_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@social_media_router.delete("/{social_media_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_social_media_controller(request: Request, social_media_id):
    try:
        response_payload = SocialMediaService.delete_social_media_service(
            social_media_id)
        logger.info(f"Deleted social media with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting social media")
        return AppServices.handle_exception(exception, is_raise=True)


@social_media_router.get("/{social_media_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_social_media_by_id_controller(request: Request, social_media_id: int):
    try:
        logger.info(f"Fetching social media details for ID: {social_media_id}")
        response_payload = SocialMediaService.get_social_media_by_id_service(
            social_media_id)
        logger.info(f"Fetched social media details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching social media details")
        return AppServices.handle_exception(exception, is_raise=True)


@social_media_router.put("/update")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_social_media_controller(request: Request,
                                   social_media_dto: UpdateSocialMediaDTO,
                                   ):
    try:
        response_payload = SocialMediaService.update_social_media_service(
            social_media_dto)
        logger.info(f"Updated social media with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)
