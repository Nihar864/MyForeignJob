import base64
import hashlib
import inspect
import re
import uuid
from datetime import datetime, timedelta
from functools import wraps

import jwt
import pyotp
from fastapi import HTTPException, Request, status

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.custom_enum.static_enum import StaticVariables
from base.dao.login.login_dao import AuthLoginDAO
from base.utils.constant import Constant
from base.utils.custom_exception import AppServices
from base.utils.date_parse_utils import DateParseUtils
from base.utils.password_hash import verify_password, hash_password
from base.vo.login_vo import AdminVO

# Constants
UUID_PATTERN = r"^[A-Za-z]{2}\d{4}$"
PHONE_PATTERN = r"^\d{10}$"
EMAIL_PATTERN = r"^\S+@\S+\.\S+$"

SECRET_KEY = Constant.SECRET_KEY

OTP_SECRET_KEY = base64.b32encode(b"SECRET_KEY").decode("utf-8")
logger = get_logger()


class LoginService:
    @staticmethod
    def get_user_by_identifier(identifier):
        auth_dao = AuthLoginDAO()

        # Define a variable to store the user and a flag for their type
        user = None
        user_type = None

        if re.match(UUID_PATTERN, identifier):
            user = auth_dao.get_admin_by_username(identifier)
            user_type = StaticVariables.MEMBER_ROLE_ENUM

        if not user:
            user = auth_dao.get_admin_by_username(identifier)
            user_type = StaticVariables.ADMIN_ROLE_ENUM if user else None
        return user, user_type

    @staticmethod
    def generate_tokens(username, user_id, role_name):
        access_token_payload = {
            "exp": datetime.utcnow()
            + timedelta(minutes=int(StaticVariables.ACCESS_TOKEN_EXPIRE_MINUTES)),
            "iat": datetime.utcnow(),
            "username": username,
            "user_id": user_id,
            "user_role": role_name,
        }
        access_token = jwt.encode(
            access_token_payload, SECRET_KEY, algorithm=StaticVariables.ALGORITHM
        )

        refresh_token_payload = {
            "iat": datetime.utcnow(),
            "username": username,
            "user_id": user_id,
            "user_role": role_name,
        }
        refresh_token = jwt.encode(
            refresh_token_payload, SECRET_KEY, algorithm=StaticVariables.ALGORITHM
        )

        return {"Access_Token": access_token, "Refresh_Token": refresh_token}

    @staticmethod
    def create_otp_details():
        totp = pyotp.TOTP(OTP_SECRET_KEY)
        token_id = uuid.uuid5(uuid.NAMESPACE_DNS, totp.now())
        expires_time = datetime.utcnow() + timedelta(minutes=2)
        send_otp = totp.now()
        combined_string = str(token_id) + totp.now()
        hashed_value = hashlib.sha256(combined_string.encode()).hexdigest()
        my_dict = dict(
            token=str(token_id),
            otp=hashed_value,
            is_used=False,
            exp_time=expires_time.strftime("%Y-%m-%d %H:%M:%S"),
            is_deleted=False,
            created_on=DateParseUtils.get_current_epoch(),
            modified_on=DateParseUtils.get_current_epoch(),
        )

        return my_dict, send_otp

    # For Admin
    @staticmethod
    def login_admin(user_info, login_pass, role_name):
        admin_vo = AdminVO()
        print("98>>>>>>>>", user_info.password)
        if user_info.is_deleted:
            print("99>>>>>>>>")
            return AppServices.app_response(
                HttpStatusCodeEnum.NOT_FOUND,
                ResponseMessageEnum.USER_NOT_FOUND,
                success=False,
                data={},
            )
        print("100>>>>>>>>", user_info.password)
        print("101>>>>>>>>", login_pass)

        if verify_password(login_pass, user_info.password):
            print("117>>>>>>>>>>>>>>")
            token_data = LoginService.generate_tokens(
                username=user_info.username,
                user_id=user_info.login_id,
                role_name=role_name,
            )
            print(">>>>>>>>>>>>>>", token_data)
            token_data.update(Role=role_name)
            logged_in_member_details = admin_vo.serialize(user_info)
            token_data.update(user_details=logged_in_member_details)

            return AppServices.app_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.LOGIN_SUCCESS,
                success=True,
                data=token_data,
            )
        return None

    @staticmethod
    def login_service(login_data):
        try:
            auth_dao = AuthLoginDAO()

            # Get username and password
            login_username = login_data.username
            login_pass = login_data.password

            # Validate a username pattern and retrieve user information
            # from the database
            user_info, user_type = LoginService.get_user_by_identifier(login_username)

            if user_info is None:
                return AppServices.app_response(
                    HttpStatusCodeEnum.UNAUTHORIZED,
                    ResponseMessageEnum.LOGIN_FAILED,
                    success=False,
                    data={},
                )

            role_name = auth_dao.get_role_by_id(user_info.role).role_name

            if user_type != role_name:
                return AppServices.app_response(
                    HttpStatusCodeEnum.UNAUTHORIZED,
                    ResponseMessageEnum.UNAUTHORIZED,
                    success=False,
                    data={},
                )

            if user_type == StaticVariables.ADMIN_ROLE_ENUM:
                return LoginService.login_admin(user_info, login_pass, role_name)
            else:
                return AppServices.app_response(
                    HttpStatusCodeEnum.UNAUTHORIZED,
                    ResponseMessageEnum.LOGIN_FAILED,
                    success=False,
                    data={},
                )

        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def get_new_access_token_service(request_data):
        try:
            auth_dao = AuthLoginDAO()
            refresh_token = request_data.refresh_token
            decoded_data = jwt.decode(
                jwt=refresh_token,
                key=SECRET_KEY,
                algorithms=[StaticVariables.ALGORITHM],
            )
            username = decoded_data.get("username")

            if not username:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.USER_NOT_FOUND,
                    success=False,
                    data={},
                )

            user_info, _ = LoginService.get_user_by_identifier(username)

            if user_info is None:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.USER_NOT_FOUND,
                    success=False,
                    data={},
                )

            role_name = auth_dao.get_role_by_id(user_info.role).role_name

            tokens = LoginService.generate_tokens(
                username=user_info.username,
                user_id=user_info.login_id,
                role_name=role_name,
            )

            return AppServices.app_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.GET_ACCESS_TOKEN,
                success=True,
                data=tokens,
            )

        except jwt.DecodeError:
            return AppServices.app_response(
                HttpStatusCodeEnum.UNAUTHORIZED,
                ResponseMessageEnum.INVALID_ACCESS_TOKEN,
                success=False,
                data={},
            )

        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    @staticmethod
    def update_password_service(request_data):
        try:
            auth_dao = AuthLoginDAO()
            username = request_data.get("username")
            old_password = request_data.get("old_password")
            new_password = request_data.get("new_password")

            user_info, _ = LoginService.get_user_by_identifier(username)

            if user_info is None or user_info.is_deleted:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    ResponseMessageEnum.USER_NOT_FOUND,
                    success=False,
                    data={},
                )

            if not verify_password(old_password, user_info.password):
                return AppServices.app_response(
                    HttpStatusCodeEnum.UNAUTHORIZED,
                    ResponseMessageEnum.INVALID_PASSWORD,
                    success=False,
                    data={},
                )

            if verify_password(new_password, user_info.password):
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST,
                    "New password must be different from the old password",
                    success=False,
                    data={},
                )

            hashed_new_password = hash_password(new_password)
            user_info.password = hashed_new_password

            auth_dao.update_password_dao(user_info)

            return AppServices.app_response(
                HttpStatusCodeEnum.OK,
                ResponseMessageEnum.PASSWORD_UPDATED,
                success=True,
                data={},
            )

        except Exception as e:
            AppServices.handle_exception(e, is_raise=True)


def login_required(required_roles=None):
    if required_roles is None:
        required_roles = []

    def decorator(route_function):
        @wraps(route_function)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.headers.get("Authorization")
            membership_id = request.headers.get("membershipId", "")

            if not token and not membership_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization credentials missing",
                )

            try:
                user_identifier = None
                user_role = None

                if token:
                    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    user_identifier = decoded_data.get("username")
                    user_role = decoded_data.get("user_role")

                    if not user_identifier or not user_role:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token payload",
                        )

                    if required_roles and user_role not in required_roles:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Access denied for role: {user_role}",
                        )
                    request.state.payload = decoded_data

                elif membership_id:
                    user_identifier = membership_id

                if not user_identifier:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User identifier missing",
                    )

                # Get user information
                result = LoginService.get_user_by_identifier(user_identifier)
                if not result or not isinstance(result, tuple) or len(result) != 2:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid user information",
                    )

                user_info, user_type = result

                if not user_info:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not found",
                    )

                role_id = getattr(user_info, "role", None)
                if role_id is None:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="User role information missing",
                    )

                auth_dao = AuthLoginDAO()
                role_obj = auth_dao.get_role_by_id(role_id)
                if not role_obj:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Role not found",
                    )

                role_name = role_obj.role_name

                # Store user context in request.state
                if inspect.iscoroutinefunction(route_function):
                    # Async route function
                    return await route_function(request=request, *args, **kwargs)
                else:
                    # Sync route function
                    return route_function(request=request, *args, **kwargs)

            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
                )

            except jwt.DecodeError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token decoding failed",
                )

            except Exception as e:
                logger.error("Unexpected error during authentication", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Authentication failure",
                )

        return wrapper

    return decorator
