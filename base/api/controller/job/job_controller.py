from fastapi import APIRouter, Request, Query

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
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def insert_job_controller(request: Request,
                          job_dto: JobDTO,
                          ):
    try:
        response_payload = JobService.insert_job_service(job_dto)

        logger.info(f"Job inserted: {response_payload}")
        return response_payload

    except Exception as e:
        logger.error(f"Error in insert_job_controller: {e}")
        return AppServices.handle_exception(e)


@job_router.get("/all")
# @login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def view_job_controller(request: Request,
                        page_number: int = Query(1, ge=1),
                        page_size: int = Query(10, ge=1),
                        search_value: str = "",
                        sort_by: str = "job_title",
                        sort_as: SortingOrderEnum = Query(
                            SortingOrderEnum.ASCENDING),
                        ):
    return JobService.get_all_job_service(
        page_number=page_number,
        page_size=page_size,
        search_value=search_value,
        sort_by=sort_by,
        sort_as=sort_as.value,
    )


@job_router.delete("/{job_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def delete_job_controller(request: Request, job_id):
    try:
        response_payload = JobService.delete_job_service(job_id)
        logger.info(f"Deleted job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error deleting country")
        return AppServices.handle_exception(exception)


@job_router.get("/{job_id}")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def get_job_by_id_controller(request: Request, job_id: int):
    try:
        logger.info(f"Fetching job details for ID: {job_id}")
        response_payload = JobService.get_job_by_id_service(job_id)
        logger.info(f"Fetched job details: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error fetching job details")
        return AppServices.handle_exception(exception)


@job_router.put("/update")
@login_required(required_roles=[StaticVariables.ADMIN_ROLE_ENUM])
def update_job_controller(request: Request, job_dto: UpdateJobDTO, ):
    try:
        response_payload = JobService.update_job_service(job_dto)
        logger.info(f"Updated job with ID: {response_payload}")
        return response_payload
    except Exception as exception:
        logger.exception("Error updating job")
        return AppServices.handle_exception(exception)
