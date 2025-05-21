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
    responses={404: {"description": "Api Endpoint Not found"}},
)


@login_router.post("/login")
async def member_login(login_dto: LoginDTO, response: Response):
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
        logger.info(f"Response for login is {response_payload}")
        return response_payload
    except Exception as exception:
        AppServices.handle_exception(exception, is_raise=True)


@login_router.put("/update_password")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
async def update_password(request: Request, password_dto: PasswordDTO,
                          response: Response):
    try:
        payload = request.state.payload
        username = payload.get("username")
        password_dto_dict = password_dto.model_dump()
        password_dto_dict["username"] = username

        response_payload = LoginService.update_password_service(
            password_dto_dict)
        logger.info(f"Updated password for user: {username}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating password")
        return AppServices.handle_exception(exception)
