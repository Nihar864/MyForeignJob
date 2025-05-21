from fastapi import APIRouter, Response, Query, Request

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.faq.faq_dto import FaqDTO, UpdateFaqDTO
from base.service.faq.faq_service import FaqService
from base.service.login.login_service import login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

faq_router = APIRouter(
    prefix="/faq",
    tags=["Faq"],
    responses={},
)


@faq_router.post("/add")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_faq_controller(request: Request,
                          faq_dto: FaqDTO,
                          response: Response,
                          ):
    try:
        if not faq_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False, )

        response_payload = FaqService.insert_faq_service(faq_dto)

        logger.info(f"Faq inserted: {response_payload}")
        return response_payload

    except Exception as exception:
        logger.error(f"Error in insert_faq_controller: {exception}")
        return AppServices.handle_exception(exception, is_raise=True)


@faq_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_faq_controller(request: Request,
                        page_number: int = Query(1, ge=1),
                        page_size: int = Query(10, ge=1),
                        search_value: str = "",
                        sort_by: str = "faq_title",
                        sort_as: SortingOrderEnum = Query(
                            SortingOrderEnum.ASCENDING)
                        ):
    return FaqService.get_all_faq_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@faq_router.delete("/{faq_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_faq_controller(request: Request, faq_id):
    try:
        response_payload = FaqService.delete_faq_service(faq_id)
        logger.info(f"Deleted faq with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting faq")
        return AppServices.handle_exception(exception, is_raise=True)


@faq_router.get("/{faq_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_faq_by_id_controller(request: Request, faq_id: int):
    try:
        logger.info(f"Fetching faq details for ID: {faq_id}")
        response_payload = FaqService.get_faq_by_id_service(faq_id)
        logger.info(f"Fetched faq details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching faq details")
        return AppServices.handle_exception(exception, is_raise=True)


@faq_router.put("/update")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_faq_controller(request: Request,
                          faq_dto: UpdateFaqDTO,
                          ):
    try:
        response_payload = FaqService.update_faq_service(faq_dto)
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating job")
        return AppServices.handle_exception(exception, is_raise=True)
