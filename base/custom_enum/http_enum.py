from enum import Enum


class HttpStatusCodeEnum(int, Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class ResponseMessageEnum(str, Enum):
    USER_REGISTERED = "User registered successfully"
    USER_IS_BLOCKED = "You are not authorized to access this resource"
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User already exists"
    USER_DELETED = "User deleted successfully"
    USER_UPDATED = "User updated successfully"
    USER_LOGIN_SUCCESS = "User logged in successfully"
    USER_LOGIN_FAILED = "User login failed"
    USER_LOGGED_OUT = "User logged out successfully"
    USER_PASSWORD_CHANGED = "User password changed successfully"
    LOGIN_FAILED = "Invalid credentials, please try again"
    LOGIN_SUCCESS = "Welcome! You've successfully logged in"
    INVALID_PASSWORD = "Old password is incorrect."
    PASSWORD_UPDATED = "Password updated successfully."
    PHONE_ALREADY_EXISTS = "Phone Number already exists"
    EMAIL_ALREADY_EXISTS = "Email already exists"
    UNAUTHORIZED = "Access denied. You are not authorized to view this"
    GET_DATA = "Data fetched successfully"
    UPDATE_DATA = "Data Updated successfully"
    NOT_FOUND = "Data not found"
    FILE_NOT_FOUND = "File not found"
    ID_NOT_FOUND = "ID not found"
    BAD_REQUEST = "Invalid request, please provide the correct information"
    INTERNAL_SERVER_ERROR = "Oops! Something went wrong"
    GET_ACCESS_TOKEN = "New access token obtained successfully"
    REFRESH_TOKEN_DOES_NOT_MATCH = "Refresh token doesn't match with your account"
    TOKEN_MISSING = "Token is missing, please provide your credentials"
    INVALID_ACCESS_TOKEN = "Oops! Invalid access token"
    ACCESS_TOKEN_EXPIRED = "Access token has expired, please log in again"
    VERIFICATION_FAILED = (
        "Your account verification is pending. Please contact support Team"
    )
    INSERT_DATA = "Data inserted successfully"
    DELETE_DATA = "Data deleted successfully"

    DUPLICATE_PDF = "PDF already exists"
    FILE_STATUS = "File process is currently in progress, so it can't be downloaded. Please try again later."
    FILE_RESTART_STATUS = "Restart is starting now."
    UPDATE_FAILED = "Update failed"

    UNEXPECTED_ERROR_MESSAGE = "An unexpected error occurred."

    ALREADY_EXISTS = "User already exists"


class SortingOrderEnum(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"
