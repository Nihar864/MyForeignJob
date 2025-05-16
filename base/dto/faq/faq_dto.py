from typing import Optional

from pydantic import BaseModel


class FaqDTO(BaseModel):
    country_id: int
    faq_title: str
    faq_description: str

    class Config:
        from_attributes = True


class UpdateFaqDTO(BaseModel):
    faq_id: int
    country_name: Optional[str] = None
    faq_title: Optional[str] = None
    faq_description: Optional[str] = None
