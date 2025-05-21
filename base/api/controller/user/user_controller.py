from fastapi import APIRouter, Response, Request, Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum, \
    SortingOrderEnum
from base.dto.user.user_dto import UserDTO, UpdateUserDTO
from base.service.user.user_service import UserService
from base.utils.custom_exception import AppServices

logger = get_logger()

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "API endpoint not found"}},
)


@user_router.post("/add")
def insert_user_controller(
        user_dto: UserDTO,
        response: Response,
):
    try:
        if not user_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST.value,
                ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )

        result = UserService.insert_user_service(user_dto)
        logger.info(f"User inserted: {result}")
        return result

    except Exception as exception:
        logger.exception("Error inserting User")
        return AppServices.handle_exception(exception)


@user_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_user_controller(request: Request,
                         page_number: int = Query(1, ge=1),
                         page_size: int = Query(10, ge=1),
                         search_value: str = "",
                         sort_by: str = "user_name",
                         sort_as: SortingOrderEnum = Query(
                             SortingOrderEnum.ASCENDING),
                         ):
    return UserService.get_all_user_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as.value,
    )


@user_router.delete("/{user_id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_user_controller(request: Request, user_id):
    try:
        response_payload = UserService.delete_user_service(user_id)
        logger.info(f"Deleted user with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting country")
        return AppServices.handle_exception(exception)


@user_router.get("/{user_id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_user_by_id_controller(request: Request, user_id: int):
    try:
        logger.info(f"Fetching user details for ID: {user_id}")
        response_payload = UserService.get_user_by_id_service(user_id)
        logger.info(f"Fetched user details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching user details")
        return AppServices.handle_exception(exception)


@user_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_user_controller(request: Request, user_dto: UpdateUserDTO, ):
    try:
        response_payload = UserService.update_user_service(user_dto)
        logger.info(f"Updated user with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating user")
        return AppServices.handle_exception(exception)
