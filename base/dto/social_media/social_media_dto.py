from typing import Optional

from pydantic import BaseModel


class SocialMediaDTO(BaseModel):
    country_id: int
    social_media_title: str
    social_media_description: str
    social_media_url: str
    social_media_status: bool

    class Config:
        from_attributes = True


class UpdateSocialMediaDTO(BaseModel):
    social_media_id: int
    country_id: Optional[int] = None
    social_media_title: Optional[str] = None
    social_media_description: Optional[str] = None
    social_media_url: Optional[str] = None
    social_media_status: Optional[bool] = None
