from typing import Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel

from base.custom_enum.http_enum import SortingOrderEnum


class JobDTO(BaseModel):
    country_id: int
    job_title: str
    job_description: str
    job_location: str
    job_salary: int
    job_status: bool

    class Config:
        from_attributes = True


class UpdateJobDTO(BaseModel):
    job_id: int
    country_id: Optional[int] = None
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    job_location: Optional[str] = None
    job_salary: Optional[str] = None
    job_status: Optional[bool] = None


class GetAllJobDTO(BaseModel):
    page_number: Optional[int] = 1
    page_size: Optional[int] = 10
    search_value: Optional[str] = ""
    sort_by: Optional[str] = "job_title"
    sort_as: SortingOrderEnum = SortingOrderEnum.ASCENDING
