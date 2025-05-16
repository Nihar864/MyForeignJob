from typing import Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel

from base.custom_enum.http_enum import SortingOrderEnum


class CountryDTO(BaseModel):
    country_name: str = (Form(...),)
    country_description: str = (Form(...),)
    show_on_homepage_status: bool = (Form(...),)
    country_status: bool = (Form(...),)
    country_currency: str = (Form(...),)
    country_image: UploadFile = (File(...),)
    country_flag_image: UploadFile = (File(...),)

    class Config:
        form_attribute = True


class UpdateCountryDTO(BaseModel):
    country_name: Optional[str] = (None,)
    country_description: Optional[str] = (None,)
    show_on_homepage_status: Optional[bool] = (None,)
    country_status: Optional[bool] = (None,)


class GetAllCountryDTO(BaseModel):
    page_number: Optional[int] = 1
    page_size: Optional[int] = 10
    search_value: Optional[str] = ""
    sort_by: Optional[str] = "country_name"
    sort_as: SortingOrderEnum = SortingOrderEnum.ASCENDING
