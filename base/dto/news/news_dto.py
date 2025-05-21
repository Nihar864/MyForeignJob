from typing import Optional

from pydantic import BaseModel


class NewsDTO(BaseModel):
    country_id: int
    news_title: str
    news_description: str
    news_url: str
    news_status: bool

    class Config:
        from_attributes = True


class UpdateNewsDTO(BaseModel):
    news_id: int
    country_id: Optional[int] = None
    news_title: Optional[str] = None
    news_description: Optional[str] = None
    news_url: Optional[str] = None
    news_status: Optional[bool] = None
