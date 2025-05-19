from fastapi import APIRouter, Response

from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dto.login.login_dto import LoginDTO
from base.service.login.login_service import LoginService
from base.utils.custom_exception import AppServices
from base.config.logger_config import get_logger

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
