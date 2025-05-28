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
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_faq_controller(
    request: Request,
    faq_dto: FaqDTO,
    response: Response,
):
    """
    Request:
        - JSON body of type FaqDTO containing:
            - faq_title: str
            - faq_description: str
        - Admin role required via JWT authentication.

    Response:
        - On Success: JSON response with status code 201 (Created) and inserted data.
        - On Failure: JSON response with appropriate error message and status code.

    Purpose:
        Insert a new FAQ entry into the system. Only accessible to ADMIN users.

    Company Name:
        Softvan Pvt Ltd

    """
    try:
        if not faq_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )

        response_payload = FaqService.insert_faq_service(faq_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Faq inserted: {response_payload}")
        return response_payload

    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@faq_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_faq_controller(
    request: Request,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "faq_title",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Request:
        - Query Parameters:
            - page_number: int (default: 1)
            - page_size: int (default: 10)
            - search_value: str (optional)
            - sort_by: str (default: "faq_title")
            - sort_as: SortingOrderEnum ("ASCENDING" or "DESCENDING")

    Response:
        - JSON list of paginated FAQ entries along with metadata.

    Purpose:
        Retrieve all FAQ records with pagination, sorting, and search capabilities.

    Company Name:
        Softvan Pvt Ltd

    """
    return FaqService.get_all_faq_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as,
    )


@faq_router.delete("/faq-id")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_faq_controller(response: Response, request: Request, faq_id):
    """
    Request:
        - Path Parameter:
            - faq_id: int
        - Admin role required via JWT authentication.

    Response:
        - On Success: JSON response confirming deletion.
        - On Failure: JSON error message with status code.

    Purpose:
        Delete a specific FAQ entry by its ID. Restricted to ADMIN users.

    Company Name:
        Softvan Pvt Ltd
    """
    try:
        response_payload = FaqService.delete_faq_service(faq_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Deleted faq with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@faq_router.get("/faq-id")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_faq_by_id_controller(response: Response, request: Request, faq_id: int):
    """
        Request:
        - Path Parameter:
            - faq_id: int
        - Admin role required via JWT authentication.

    Response:
        - On Success: JSON object of the requested FAQ.
        - On Failure: JSON error message with status code.
    Purpose:
        Retrieve detailed information for a specific FAQ entry using its ID.

    Company Name:
        Softvan Pvt Ltd
    """
    try:
        response_payload = FaqService.get_faq_by_id_service(faq_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Fetched faq details: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)


@faq_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_faq_controller(
    response: Response,
    request: Request,
    faq_dto: UpdateFaqDTO,
):
    """
    Request:
        - JSON body of type UpdateFaqDTO containing:
            - faq_id: int
            - faq_title: str
            - faq_description: str
        - Admin role required via JWT authentication.

    Response:
        - On Success: JSON response confirming the update.
        - On Failure: JSON error message with status code.

    Purpose:
        Update an existing FAQ entry using the provided data. Only ADMIN users are authorized.

    Company Name:
        Softvan Pvt Ltd
    """
    try:
        response_payload = FaqService.update_faq_service(faq_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception, is_raise=True)
