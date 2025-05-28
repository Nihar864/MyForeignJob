from fastapi import APIRouter, Response, Request, Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import (
    HttpStatusCodeEnum,
    ResponseMessageEnum,
    SortingOrderEnum,
)
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
    """
    Request:
        - user_dto: UserDTO object containing user details.
        - response: FastAPI Response object for setting status codes.

    Response:
        - On success, returns the inserted user data.
        - On failure or invalid input, returns appropriate error response.

    Purpose:
        Insert a new user record into the system.

    Company Name:
        Softvan Pvt Ltd
    """
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
        return AppServices.handle_exception(exception)


@user_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_user_controller(
    request: Request,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "user_name",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Request:
        - request: FastAPI Request object.
        - page_number: Page number for pagination (default 1).
        - page_size: Number of users per page (default 10).
        - search_value: String to filter users by matching criteria (default empty).
        - sort_by: Field name to sort the results (default "user_name").
        - sort_as: Sorting order, ascending or descending (default ascending).

    Response:
        - Returns a paginated list of users matching the search and sorting criteria.

    Purpose:
        Retrieve a paginated list of users with optional search and sorting.

    Company Name:
        Softvan Pvt Ltd
    """
    return UserService.get_all_user_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as.value,
    )


@user_router.delete("/{user-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_user_controller(response: Response, request: Request, user_id):
    """
    Request:
        - request: FastAPI Request object.
        - user_id: Integer representing the user ID to be deleted.

    Response:
        - On success, returns confirmation of deletion.
        - On failure, returns appropriate error response.

    Purpose:
        Delete a user by their unique identifier.

    Company Name:
        Softvan Pvt Ltd
    """
    try:
        response_payload = UserService.delete_user_service(user_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Deleted user with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@user_router.get("/{user-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_user_by_id_controller(response: Response, request: Request, user_id: int):
    """
    Request:
        - request: FastAPI Request object.
        - user_id: Integer representing the user ID to retrieve.

    Response:
        - Returns detailed information of the user.
        - On failure, returns appropriate error response.

    Purpose:
        Retrieve user details by their unique identifier.

    Company Name:
        Softvan Pvt Ltd
    """
    try:
        logger.info(f"Fetching user details for ID: {user_id}")
        response_payload = UserService.get_user_by_id_service(user_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Fetched user details: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@user_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_user_controller(
    response: Response,
    request: Request,
    user_dto: UpdateUserDTO,
):
    """
    Request:
        - request: FastAPI Request object.
        - user_dto: UpdateUserDTO object containing updated user information.

    Response:
        - Returns the updated user data on success.
        - On failure, returns appropriate error response.

    Purpose:
        Update existing user details.

    Company Name:
        Softvan Pvt Ltd
    """
    try:
        response_payload = UserService.update_user_service(user_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated user with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)
