import re

from fastapi import FastAPI

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.user.user_dao import UserDAO
from base.utils.custom_exception import AppServices
from base.vo.user_vo import UserVO

logger = get_logger()

app = FastAPI()


class UserService:
    @staticmethod
    def Validation_service(user_dto):
        """
        Validate user input data.

        Request:
            user_dto (UserVO): Data transfer object containing user input fields
                               such as user_name, user_email, user_phone, country_id.

        Response:
            On validation failure, returns a formatted error response indicating
            the specific invalid field (name, email, phone, or country).
            On success, returns a tuple of validated fields:
            (name, email, phone, country_vo).

        Purpose:
            Ensures that user data complies with format requirements and that
            user email and phone do not already exist in the database.
            Also verifies the validity of the country ID.

        Company:
            Softvan Pvt Ltd
        """
        # Name Validation
        name = user_dto.user_name.strip()
        if not re.fullmatch(r"[A-Za-z ]{3,}", name):
            logger.warning("Invalid name format received: %s", name)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                "Invalid name. Only letters and spaces allowed, min length 3.",
                success=False,
            )

        # Email Validation
        email = user_dto.user_email.strip()
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            logger.warning("Invalid email format received: %s", email)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST, "Invalid email format.", success=False
            )

        # Check Existing User Email
        existing_user = UserDAO.check_existing_user_email(email)
        if existing_user:
            logger.info("Email already exists: %s", email)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.EMAIL_ALREADY_EXISTS,
                success=False,
            )

        # Phone Validation
        phone = user_dto.user_phone.strip()
        if not re.fullmatch(r"\d{10}", phone):
            logger.warning("Invalid phone format received: %s", phone)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                "Phone must be a 10-digit number.",
                success=False,
            )

        # Check Existing User Phone
        existing_user = UserDAO.check_existing_user_phone(phone)
        if existing_user:
            logger.info("Phone already exists: %s", phone)
            return AppServices.app_response(
                HttpStatusCodeEnum.BAD_REQUEST,
                ResponseMessageEnum.PHONE_ALREADY_EXISTS,
                success=False,
            )

        country_vo = CountryDAO.get_country_by_id_dao(user_dto.country_id)
        if not country_vo:
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                "try another country",
                success=False,
                data={},
            )

        return name, email, phone, country_vo

    @staticmethod
    def insert_user_service(user_dto):
        """
        Validate user data and insert a new user into the system.

        Request:
            user_dto (UserVO): Data transfer object containing user details to be inserted.

        Response:
            On validation failure, returns the corresponding error response.
            On success, returns a success response with the inserted user data.

        Purpose:
            To register a new user by validating inputs and persisting the user
            record into the database.

        Company:
            Softvan Pvt Ltd
        """
        logger.info("Initiating user registration process...")

        validated_data = UserService.Validation_service(user_dto)

        if not isinstance(validated_data, tuple):
            return validated_data

        name, email, phone, country_vo = validated_data

        # Insert New User
        logger.debug("Creating UserVO and inserting into database...")
        user_vo = UserVO()
        user_vo.user_name = name
        user_vo.user_email = email
        user_vo.user_phone = phone
        user_vo.user_country_id = country_vo.country_id
        user_vo.user_country_name = country_vo.country_name

        user_record = UserDAO.insert_user_dao(user_vo)

        if not user_record:
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
            data={user_record},
        )

    @staticmethod
    def get_all_user_service(page_number, page_size, search_value, sort_by, sort_as):
        """
        Retrieve a paginated, sorted, and searchable list of users.

        Request:
            page_number (int): Page number for pagination.
            page_size (int): Number of records per page.
            search_value (str): Search keyword for filtering users.
            sort_by (str): Field name to sort by.
            sort_as (str): Sort direction, e.g., 'asc' or 'desc'.

        Response:
            Returns a paginated list of users matching search criteria, or an error response if none found.

        Purpose:
            Provides a flexible endpoint to query user records with pagination, searching, and sorting.

        Company:
            Softvan Pvt Ltd
        """
        try:
            result = UserDAO.get_all_user_dao(
                search_value=search_value,
                page_number=page_number,
                page_size=page_size,
                sort_by=sort_by,
                sort_as=sort_as,
            )

            if not result["items"]:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=result,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_user_service(user_id):
        """
        Soft delete a user by marking their record as deleted.

        Request:
            user_id (int): Identifier of the user to be deleted.

        Response:
            Success response if user is soft deleted; error response if user not found or failure occurs.

        Purpose:
            Implements a non-destructive deletion method by marking the user record as deleted without physically removing it.

        Company:
            Softvan Pvt Ltd
        """
        try:
            delete_user_data = UserDAO.delete_user_dao(user_id)

            if not delete_user_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_user_data.is_deleted = True  # Soft delete

            logger.info("Deleted user with ID: %s", user_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_user_data,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_user_by_id_service(user_id):
        """
        Retrieve details of a user given their ID.

        Request:
            user_id (int): Unique identifier of the user.

        Response:
            Returns user details if found; error response if user does not exist.

        Purpose:
            Facilitates fetching individual user information for viewing or editing.

        Company:
            Softvan Pvt Ltd
        """
        try:
            user_detail = UserDAO.get_user_by_id_dao(user_id)

            if not user_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched user detail for ID: %s", user_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=user_detail,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_user_service(user_dto):
        """
        Update an existing user's information.

        Request:
            user_dto (UserVO): Data transfer object containing updated user fields including user_id.

        Response:
            Returns success response with updated user data on success; error response if user does not exist or update fails.

        Purpose:
            Allows modification of user attributes while validating linked data like country.

        Company:
            Softvan Pvt Ltd
        """
        try:
            existing_user = UserDAO.get_user_by_id_dao(user_dto.user_id)

            if not existing_user:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if user_dto.user_name is not None:
                existing_user.user_name = user_dto.user_name

            if user_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(user_dto.country_id)
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_user.user_country_id = country_vo.country_id
                existing_user.user_country_name = country_vo.country_name

            if user_dto.user_email is not None:
                existing_user.user_email = user_dto.user_email

            if user_dto.user_phone is not None:
                existing_user.user_phone = user_dto.user_phone

            # Step 3: Persist updated data
            updated_user = UserDAO.update_user_dao(existing_user)

            if not updated_user:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated user with ID: %s", user_dto.user_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_user,
            )

        except Exception as exception:
            return AppServices.handle_exception(exception)
