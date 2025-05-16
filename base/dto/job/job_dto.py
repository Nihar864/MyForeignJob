from typing import Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel

from base.custom_enum.http_enum import SortingOrderEnum


class GetAllJobDTO(BaseModel):
    page_number: Optional[int] = 1
    page_size: Optional[int] = 10
    search_value: Optional[str] = ""
    sort_by: Optional[str] = "job_title"
    sort_as: SortingOrderEnum = SortingOrderEnum.ASCENDING
