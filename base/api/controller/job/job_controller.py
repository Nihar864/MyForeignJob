from typing import Optional

from fastapi import APIRouter, Form, Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.service.job.job_service import JobService
from base.utils.custom_exception import AppServices

logger = get_logger()

job_router = APIRouter(
    prefix="/job",
    tags=["Job"],
    responses={},
)


@job_router.post("/add")
# @login_required()
def insert_job_controller(
    country_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_location: str = Form(...),
    job_salary: int = Form(...),
    job_status: bool = Form(...),
):
    try:
        response_payload = JobService.insert_job_service(
            job_title=job_title,
            country_name=country_name,
            job_description=job_description,
            job_location=job_location,
            job_salary=job_salary,
            job_status=job_status,
        )

        logger.info(f"Job inserted: {response_payload}")
        return response_payload

    except Exception as e:
        logger.error(f"Error in insert_job_controller: {e}")
        return AppServices.handle_exception(e)


@job_router.get("/all")
# @login_required()
def view_job_controller(
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "job_title",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    return JobService.get_all_job_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as.value,
    )


@job_router.delete("/{job_id}")
# @login_required()
def delete_job_controller(job_id):
    try:
        response_payload = JobService.delete_job_service(job_id)
        logger.info(f"Deleted job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting country")
        return AppServices.handle_exception(exception)


@job_router.get("/{job_id}")
# @login_required()
def get_job_by_id_controller(job_id: int):
    try:
        logger.info(f"Fetching job details for ID: {job_id}")
        response_payload = JobService.get_job_by_id_service(job_id)
        logger.info(f"Fetched job details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching job details")
        return AppServices.handle_exception(exception)


@job_router.put("/update")
# @login_required()
def update_job_controller(
    job_id: int = Form(...),
    job_title: Optional[str] = Form(...),
    job_description: Optional[str] = Form(...),
    country_name: Optional[str] = Form(...),
    job_location: Optional[str] = Form(...),
    job_salary: Optional[int] = Form(...),
    job_status: Optional[bool] = Form(...),
):
    try:
        response_payload = JobService.update_job_service(
            job_id=job_id,
            job_title=job_title,
            country_name=country_name,
            job_description=job_description,
            job_location=job_location,
            job_salary=job_salary,
            job_status=job_status,
        )
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating job")
        return AppServices.handle_exception(exception)
