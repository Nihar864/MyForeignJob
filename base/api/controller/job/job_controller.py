from fastapi import APIRouter, Request, Query, Response

from base.config.logger_config import get_logger
from base.custom_enum.http_enum import SortingOrderEnum
from base.custom_enum.static_enum import StaticVariables
from base.dto.job.job_dto import JobDTO, UpdateJobDTO
from base.service.job.job_service import JobService
from base.service.login.login_service import login_required
from base.utils.custom_exception import AppServices

logger = get_logger()

job_router = APIRouter(
    prefix="/job",
    tags=["Job"],
    responses={},
)


@job_router.post("/add")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_job_controller(
    response: Response,
    request: Request,
    job_dto: JobDTO,
):
    """
    Request:
        - job_dto (JobDTO): JSON payload with job data to be inserted.

    Response:
        - JSON: Contains success status and job data or error details.

    Purpose:
        - To insert a new job into the database.

    Company Name: Softvan Pvt Ltd
    """
    try:
        response_payload = JobService.insert_job_service(job_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Job inserted: {response_payload}")
        return response_payload

    except Exception as e:
        return AppServices.handle_exception(e)


@job_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_job_controller(
    request: Request,
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    search_value: str = "",
    sort_by: str = "job_title",
    sort_as: SortingOrderEnum = Query(SortingOrderEnum.ASCENDING),
):
    """
    Request:
        - page_number (int): Page index for paginated results.
        - page_size (int): Number of records per page.
        - search_value (str): Keyword to filter jobs by title.
        - sort_by (str): Field to sort on (e.g., job_title).
        - sort_as (SortingOrderEnum): Sort direction (ASCENDING/DESCENDING).

    Response:
        - JSON: Paginated list of job records.

    Purpose:
        - To retrieve all jobs with pagination, filtering, and sorting options.

    Company Name: Softvan Pvt Ltd
    """
    return JobService.get_all_job_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as.value,
    )


@job_router.delete("/{job-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_job_controller(response: Response, request: Request, job_id):
    """
    Request:
        - job_id (int): Unique identifier of the job to be deleted.

    Response:
        - JSON: Confirmation message or error detail.

    Purpose:
        - To delete a job from the system using its ID.

    Company Name: Softvan Pvt Ltd
    """
    try:
        response_payload = JobService.delete_job_service(job_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Deleted job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@job_router.get("/{job-id}")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_job_by_id_controller(response: Response, request: Request, job_id: int):
    """
    Request:
        - job_id (int): Unique identifier for the job to be retrieved.

    Response:
        - JSON: Job data or appropriate error message.

    Purpose:
        - To fetch a specific job's details using its ID.

    Company Name: Softvan Pvt Ltd
    """
    try:
        logger.info(f"Fetching job details for ID: {job_id}")
        response_payload = JobService.get_job_by_id_service(job_id)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Fetched job details: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)


@job_router.put("/update")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_job_controller(
    response: Response,
    request: Request,
    job_dto: UpdateJobDTO,
):
    """
    Request:
        - job_dto (UpdateJobDTO): JSON payload containing updated job information.

    Response:
        - JSON: Success message with updated job details or error info.

    Purpose:
        - To update an existing job's details.

    Company Name: Softvan Pvt Ltd
    """
    try:
        response_payload = JobService.update_job_service(job_dto)
        response.status_code = response_payload.get("status_code")
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        return AppServices.handle_exception(exception)
