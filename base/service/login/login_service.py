# path: base/service/login/login_service.py

from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Request, Response
from functools import wraps

from base.config.logger_config import get_logger
from base.utils.constant import Constant

logger = get_logger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginService:
    @staticmethod
    def generate_tokens(user_id: int, username: str, user_role: str):
        access_payload = {
            "user_id": user_id,
            "username": username,
            "user_role": user_role,
            "exp": datetime.utcnow() + timedelta(seconds=Constant.ACCESS_TOKEN_EXP),
        }

        refresh_payload = {
            "user_id": user_id,
            "username": username,
            "user_role": user_role,
            "exp": datetime.utcnow() + timedelta(seconds=Constant.REFRESH_TOKEN_EXP),
        }

        access_token = jwt.encode(
            access_payload, Constant.SECRET_KEY, algorithm=Constant.HASH_ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_payload, Constant.SECRET_KEY, algorithm=Constant.HASH_ALGORITHM
        )

        return access_token, refresh_token

    @staticmethod
    def decode_access_token(token: str):
        try:
            return jwt.decode(
                token, Constant.SECRET_KEY, algorithms=[Constant.HASH_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Access token expired")
        except jwt.DecodeError:
            raise ValueError("Invalid access token")


def login_required():
    def decorator(route_function):
        @wraps(route_function)
        def wrapper(request: Request, response: Response, *args, **kwargs):
            token = request.headers.get("Authorization") or request.cookies.get(
                "access_token"
            )

            if not token:
                raise HTTPException(
                    status_code=401, detail="Authorization token missing"
                )

            if token.startswith("Bearer "):
                token = token.replace("Bearer ", "")

            try:
                decoded = jwt.decode(
                    token, Constant.SECRET_KEY, algorithms=[Constant.HASH_ALGORITHM]
                )
                request.state.user = decoded
                logger.info(
                    f"Authenticated user {decoded['user_id']} with role {decoded['user_role']}"
                )
                return route_function(request, response, *args, **kwargs)

            except jwt.ExpiredSignatureError:
                refresh_token = request.cookies.get("refresh_token")
                if not refresh_token:
                    raise HTTPException(
                        status_code=401, detail="Session expired. Please login again."
                    )

                try:
                    decoded_refresh = jwt.decode(
                        refresh_token,
                        Constant.SECRET_KEY,
                        algorithms=[Constant.HASH_ALGORITHM],
                    )
                    new_access, new_refresh = LoginService.generate_tokens(
                        decoded_refresh["user_id"],
                        decoded_refresh["username"],
                        decoded_refresh["user_role"],
                    )
                    response.set_cookie(
                        "access_token",
                        new_access,
                        max_age=Constant.ACCESS_TOKEN_EXP,
                        httponly=True,
                    )
                    response.set_cookie(
                        "refresh_token",
                        new_refresh,
                        max_age=Constant.REFRESH_TOKEN_EXP,
                        httponly=True,
                    )

                    return route_function(request, response, *args, **kwargs)

                except jwt.ExpiredSignatureError:
                    raise HTTPException(
                        status_code=401, detail="Refresh token expired. Login again."
                    )
                except jwt.DecodeError:
                    raise HTTPException(
                        status_code=401, detail="Invalid refresh token."
                    )

            except jwt.DecodeError:
                raise HTTPException(status_code=401, detail="Invalid token format")

        return wrapper

    return decorator
