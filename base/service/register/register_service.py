import bcrypt
from fastapi import FastAPI

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.login.login_dao import LoginDAO
from base.dao.register.register_dao import RegisterDAO
from base.utils.custom_exception import AppServices

from base.vo.login_vo import LoginVO
from base.vo.register_vo import RegisterVO

logger = get_logger()
app = FastAPI()


class RegisterService:
    @staticmethod
    def register_user(register_dto):
        """Handles user registration logic."""

        existing_user = RegisterDAO.check_existing_user(register_dto.registerName)
        if existing_user:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                "try another username",
                success=False,
                data={},
            )

        # Create and insert registered user
        register_user = RegisterVO(
            registerName=register_dto.registerName,
            registerEmail=register_dto.registerEmail,
            registerPhone=register_dto.registerPhone,
        )

        register_record = RegisterDAO.insert_register_user(register_user)
        if not register_record:
            return AppServices.app_response(
                HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                ResponseMessageEnum.NOT_FOUND,
                success=False,
                data={},
            )

        return AppServices.app_response(
            HttpStatusCodeEnum.CREATED,
            ResponseMessageEnum.INSERT_DATA,
            success=True,
            data={register_record},
        )
