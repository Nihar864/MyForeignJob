# path: base/controller/login_router.py

from fastapi import APIRouter, HTTPException, Response
from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dto.login.login_dto import LoginDTO
from base.service.login.login_service import LoginService
from base.utils.custom_exception import AppServices
from base.utils.constant import Constant

logger = get_logger()

login_router = APIRouter(
    prefix="/auth",
    tags=["Login"],
    responses={404: {"description": "API endpoint not found"}},
)


@login_router.post("/user_login")
def admin_login(login_dto: LoginDTO, response: Response):
    try:
        if (
            login_dto.loginUsername != Constant.ADMIN_USERNAME
            or login_dto.loginPassword != Constant.ADMIN_PASSWORD
        ):
            return AppServices.app_response(
                status_code=HttpStatusCodeEnum.BAD_REQUEST.value,
                message=ResponseMessageEnum.NOT_FOUND.value,
                success=False,
            )

        access_token, refresh_token = LoginService.generate_tokens(
            user_id=0, username=Constant.ADMIN_USERNAME, user_role="admin"
        )

        response.set_cookie(
            "access_token",
            access_token,
            max_age=Constant.ACCESS_TOKEN_EXP,
            httponly=True,
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=Constant.REFRESH_TOKEN_EXP,
            httponly=True,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "message": "Admin login successful",
        }

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value,
            detail=ResponseMessageEnum.USER_LOGIN_FAILED.value,
        )
