from typing import Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel


class CountryDTO(BaseModel):
    country_name: str = Form(...),
    country_description: str = Form(...),
    show_on_homepage_status: bool = Form(...),
    country_status: bool = Form(...),
    country_currency: str = Form(...),
    country_image: UploadFile = File(...),
    country_flag_image: UploadFile = File(...),

    class Config:
        form_attribute = True


class UpdateCountryDTO(BaseModel):
    country_name: Optional[str] = (None,)
    country_description: Optional[str] = (None,)
    show_on_homepage_status: Optional[bool] = (None,)
    country_status: Optional[bool] = (None,)
