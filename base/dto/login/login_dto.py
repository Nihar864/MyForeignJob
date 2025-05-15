from pydantic import BaseModel


class LoginDTO(BaseModel):
    loginUsername: str
    loginPassword: str
