from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    country_id: int
    user_name: str
    user_email: str
    user_phone: str

    class Config:
        from_attributes = True


class UpdateUserDTO(BaseModel):
    user_id: int
    country_id: Optional[int] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
