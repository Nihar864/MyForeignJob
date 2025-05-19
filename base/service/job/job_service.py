from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.country.country_dao import CountryDAO
from base.dao.job.job_dao import JobDAO
from base.dto.job.job_dto import GetAllJobDTO
from base.utils.custom_exception import AppServices
from base.vo.job_vo import JobVO

logger = get_logger()


class JobService:

    @staticmethod
    def insert_job_service(job_dto):
        try:
            country_vo = CountryDAO.get_country_by_id_dao(job_dto.country_id)
            if not country_vo:
                return AppServices.app_response(
                    HttpStatusCodeEnum.NOT_FOUND,
                    "this country is not exist",
                    success=False,
                    data={},
                )

            job_vo = JobVO()
            job_vo.job_country_id = country_vo.country_id
            job_vo.job_country_name = country_vo.country_name
            job_vo.job_title = job_dto.job_title
            job_vo.job_description = job_dto.job_description
            job_vo.job_location = job_dto.job_location
            job_vo.job_salary = job_dto.job_salary
            job_vo.job_status = job_dto.job_status

            job_insert_data = JobDAO.insert_job_dao(job_vo)

            if not job_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted job: %s", job_vo.job_title)
            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.INSERT_DATA.value,
                success=True,
                data=job_insert_data,
            )

        except Exception as exception:
            logger.exception("Error inserting job")
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_all_job_service(page_number, page_size, search_value, sort_by, sort_as):
        try:
            result = JobDAO.get_all_job_dao(
                search_value=search_value,
                page_number=page_number,
                page_size=page_size,
                sort_by=sort_by,
                sort_as=sort_as,
            )

            if not result["items"]:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            return AppServices.app_response(
                HttpStatusCodeEnum.OK.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=result,
            )

        except Exception as exception:
            logger.exception("Error fetching all jobs")
            return AppServices.handle_exception(exception)

    @staticmethod
    def delete_job_service(job_id):
        """Soft delete a job by ID."""
        try:
            delete_job_data = JobDAO.delete_job_dao(job_id)

            if not delete_job_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_job_data.is_deleted = True  # Soft delete

            logger.info("Deleted job with ID: %s", job_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_job_data,
            )

        except Exception as exception:
            logger.exception("Error deleting job with ID: %s", job_id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_job_by_id_service(job_id):
        """Retrieve job details for a given ID."""
        try:
            job_detail = JobDAO.get_job_by_id_dao(job_id)

            if not job_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched job detail for ID: %s", job_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=job_detail,
            )

        except Exception as exception:
            logger.exception("Error retrieving job with ID: %s", job_id)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_job_service(job_dto):
        try:
            existing_job = JobDAO.get_job_by_id_dao(job_dto.job_id)

            if not existing_job:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if job_dto.job_title is not None:
                existing_job.job_title = job_dto.job_title

            if job_dto.country_id is not None:
                country_vo = CountryDAO.get_country_by_id_dao(job_dto.country_id)
                if not country_vo:
                    return AppServices.app_response(
                        HttpStatusCodeEnum.NOT_FOUND,
                        "try another country",
                        success=False,
                        data={},
                    )
                existing_job.job_country_id = country_vo.country_id
                existing_job.job_country_name = country_vo.country_name

            if job_dto.job_description is not None:
                existing_job.job_description = job_dto.job_description

            if job_dto.job_location is not None:
                existing_job.job_location = job_dto.job_location

            if job_dto.job_salary is not None:
                existing_job.job_salary = job_dto.job_salary

            if job_dto.job_status is not None:
                existing_job.job_status = job_dto.job_status

            # Step 3: Persist updated data
            updated_job = JobDAO.update_job_dao(existing_job)

            if not updated_job:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated job with ID: %s", job_dto.job_id)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_job,
            )

        except Exception as exception:
            logger.exception("Error updating job")
            return AppServices.handle_exception(exception)
