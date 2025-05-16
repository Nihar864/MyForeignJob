from pydantic import BaseModel


class RegisterDTO(BaseModel):
    register_name: str
    register_email: str
    register_phone: str

    class Config:
        from_attributes = True
