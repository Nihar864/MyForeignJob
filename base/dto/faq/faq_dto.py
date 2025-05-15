from pydantic import BaseModel


class FaqDTO(BaseModel):
    country_name: str
    faq_title: str
    faq_description: str

    class Config:
        from_attributes = True