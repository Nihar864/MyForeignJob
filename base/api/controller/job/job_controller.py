from typing import Optional

from fastapi import APIRouter, Request, Response, UploadFile, File, Form, Query

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.utils.custom_exception import AppServices
from base.service.job.job_service import JobService

logger = get_logger()

job_router = APIRouter(
    prefix="/job",
    tags=["Job"],
    responses={},
)


@job_router.post("/add")
# @login_required()
def insert_job_controller(
    countryName: str = Form(...),
    jobTitle: str = Form(...),
    jobDescription: str = Form(...),
    joblocation: str = Form(...),
    jobSalary: int = Form(...),
    jobStatus: bool = Form(...),
):
    try:
        response_payload = JobService.insert_job_service(
            jobTitle=jobTitle,
            countryName=countryName,
            jobDescription=jobDescription,
            joblocation=joblocation,
            jobSalary=jobSalary,
            jobStatus=jobStatus,
        )

        logger.info(f"Job inserted: {response_payload}")
        return response_payload

    except Exception as e:
        logger.error(f"Error in insert_job_controller: {e}")
        return AppServices.handle_exception(e)


@job_router.get("/all")
# @login_required()
def get_all_job_service(
        pageNumber: int = Query(1, ge=1),
        pageSize: int = Query(10, ge=1),
        searchValue: str = "",
        sortBy: str = "jobTitle",
        sortAs: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING)
):
    return JobService.get_all_job_service(
        pageNumber=pageNumber,
        pageSize=pageSize,
        searchValue=searchValue,
        sortBy=sortBy,
        sortAs=sortAs.value
    )


@job_router.delete("/{jobId}")
# @login_required()
def delete_job_controller(jobId):
    try:
        response_payload = JobService.delete_job_service(jobId)
        logger.info(f"Deleted job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting country")
        return AppServices.handle_exception(exception)


@job_router.get("/{jobId}")
# @login_required()
def get_job_by_id_controller(jobId: int):
    try:
        logger.info(f"Fetching job details for ID: {jobId}")
        response_payload = JobService.get_job_by_id_service(jobId)
        logger.info(f"Fetched job details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching job details")
        return AppServices.handle_exception(exception)


@job_router.put("/update")
# @login_required()
def update_job_controller(
    jobId: int = Form(...),
    jobTitle: Optional[str] = Form(...),
    jobDescription: Optional[str] = Form(...),
    countryName: Optional[str] = Form(...),
    jobLocation: Optional[str] = Form(...),
    jobSalary: Optional[int] = Form(...),
    jobStatus: Optional[bool] = Form(...),
):
    try:
        response_payload = JobService.update_job_service(
            jobId=jobId,
            jobTitle=jobTitle,
            countryName=countryName,
            jobDescription=jobDescription,
            jobLocation=jobLocation,
            jobSalary=jobSalary,
            jobStatus=jobStatus,
        )
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating job")
        return AppServices.handle_exception(exception)
