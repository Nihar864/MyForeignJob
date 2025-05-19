from enum import Enum


class StaticVariables(str, Enum):
    """
    Class: StaticVariables
    Author: Tarun Mondal
    Designation: Software Engineer

    This class defines static variables using Enum for your application.

    Attributes:
        ALGORITHM (str): The hashing algorithm to be used.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
        ADMIN_ROLE_ENUM (str): The role for administrators.
        MEMBER_ROLE_ENUM (str): The role for regular members.
        SUB_MEMBER_ROLE_ENUM (str): The role for sub-members.
    """

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    ADMIN_ROLE_ENUM = "ADMIN"
    MEMBER_ROLE_ENUM = "member"
    SUB_MEMBER_ROLE_ENUM = "submember"
