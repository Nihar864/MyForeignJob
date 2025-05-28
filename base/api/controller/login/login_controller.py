from fastapi import APIRouter, Response, Request

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.login.login_dto import LoginDTO, PasswordDTO
from base.service.login.login_service import LoginService, login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

login_router = APIRouter(
    prefix="/auth",
    tags=["Login"],
    responses={404: {"description": "API Endpoint Not Found"}},
)


@login_router.post("/login")
async def member_login(login_dto: LoginDTO, response: Response):
    """
    POST /auth/login

    Purpose:
        This endpoint handles the authentication process for users by validating their credentials.
        It is responsible for generating access and refresh tokens for session management.

    Request:
        - login_dto (LoginDTO): A Pydantic DTO containing user credentials such as username and password.
        - response (Response): The FastAPI response object used to manipulate response metadata.

    Response:
        - JSON object containing login status, JWT tokens, user details, and success flag.
        - On failure, returns appropriate HTTP error response with message and empty data object.

    Company: Softvan Pvt Ltd
    """
    try:
        if not login_dto:
            response.status_code = HttpStatusCodeEnum.BAD_REQUEST
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.BAD_REQUEST,
                success=False,
                data={},
            )

        response_payload = LoginService.login_service(login_dto)
        print("respomse_payload",response_payload)
        logger.info(f"Response for login is {response_payload}")
        return response_payload
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)


@login_router.put("/update_password")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
async def update_password(
    request: Request, password_dto: PasswordDTO, response: Response
):
    """
    PUT /auth/update_password

    Purpose:
        This secured endpoint allows authenticated administrators to update their own password.
        Access is restricted to users with ADMIN role only.

    Request:
        - request (Request): The FastAPI request object used to extract the JWT payload.
        - password_dto (PasswordDTO): A Pydantic DTO containing the old and new password fields.
        - response (Response): The FastAPI response object for setting metadata if necessary.

    Response:
        - JSON object indicating whether the password update was successful.
        - On failure, logs the error and returns a structured error response.

    Company: Softvan Pvt Ltd
    """
    try:
        payload = request.state.payload
        username = payload.get("username")
        password_dto_dict = password_dto.model_dump()
        password_dto_dict["username"] = username

        response_payload = LoginService.update_password_service(password_dto_dict)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated password for user: {username}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating password")
        return AppServices.handle_exception(exception)
