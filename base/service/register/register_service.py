import re
from fastapi import FastAPI
from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.utils.custom_exception import AppServices
from base.dao.register.register_dao import RegisterDAO
from base.vo.register_vo import RegisterVO

# Logger
logger = get_logger()

# FastAPI app instance
app = FastAPI()


class RegisterService:
    @staticmethod
    def register_user(register_dto):
        """Validates and registers a user."""
        logger.info("Initiating user registration process...")

        # -------------------
        # Name Validation
        # -------------------
        name = register_dto.register_name.strip()
        if not re.fullmatch(r"[A-Za-z ]{3,}", name):
            logger.warning("Invalid name format received: %s", name)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                "Invalid name. Only letters and spaces allowed, min length 3.",
                success=False
            )

        # -------------------
        # Email Validation
        # -------------------
        email = register_dto.register_email.strip()
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            logger.warning("Invalid email format received: %s", email)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                "Invalid email format.",
                success=False
            )

        # -------------------
        # Phone Validation
        # -------------------
        phone = register_dto.register_phone.strip()
        if not re.fullmatch(r"\d{10}", phone):
            logger.warning("Invalid phone format received: %s", phone)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                "Phone must be a 10-digit number.",
                success=False
            )

        # -------------------
        # Check Existing User
        # -------------------
        logger.debug("Checking if user already exists: %s", name)
        existing_user = RegisterDAO.check_existing_user(name)
        if existing_user:
            logger.info("Username already exists: %s", name)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.USER_ALREADY_EXISTS,
                success=False
            )

        # Insert New User
        logger.debug("Creating RegisterVO and inserting into database...")
        register_vo = RegisterVO(
            register_name=name,
            register_email=email,
            register_phone=phone,
        )
        register_record = RegisterDAO.insert_register_user(register_vo)

        if not register_record:
            logger.error("Database insertion failed for user: %s", name)
            return AppServices.app_response(
                HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                ResponseMessageEnum.NOT_FOUND,
                success=False,
            )

        logger.info("User registration successful for: %s", name)
        return AppServices.app_response(
            HttpStatusCodeEnum.CREATED,
            ResponseMessageEnum.INSERT_DATA,
            success=True,
            data={register_record},
        )
