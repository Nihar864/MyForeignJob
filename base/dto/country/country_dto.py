from fastapi import Form, UploadFile, File
from pydantic import BaseModel
from typing import Optional


# class CountryDTO(BaseModel):
#     countryName= str,
#     countryDescription =  str,
#     homepageStatus = bool,
#     countryStatus = bool ,
#     # countryImage: UploadFile = File(...),
#
#     class Config:
#         form_attribute = True


class UpdateCountryDTO(BaseModel):
    countryName: Optional[str] = (None,)
    countryDescription: Optional[str] = (None,)
    showOnHomepageStatus: Optional[bool] = (None,)
    countryStatus: Optional[bool] = (None,)
