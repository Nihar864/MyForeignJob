from pydantic import BaseModel


class LoginDTO(BaseModel):
    login_username: str
    login_password: str
