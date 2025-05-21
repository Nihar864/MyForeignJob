from pydantic import BaseModel


class LoginDTO(BaseModel):
    """
    Data transfer object for user login.
    Author: Tarun Mondal
    Designation: Software Engineer

    Attributes:
        username (str): The username provided by the user.
        password (str): The password provided by the user.
    """

    username: str
    password: str


class PasswordDTO(BaseModel):
    old_password: str
    new_password: str
