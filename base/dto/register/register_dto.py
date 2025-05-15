from pydantic import BaseModel


class RegisterDTO(BaseModel):
    registerName: str
    registerEmail: str
    registerPhone: str

    class Config:
        from_attributes = True
