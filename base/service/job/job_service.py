from base.config.logger_config import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
from base.dao.job.job_dao import JobDAO
from base.utils.custom_exception import AppServices
from base.vo.job_vo import JobVO

logger = get_logger()


class JobService:

    @staticmethod
    def insert_job_service(
            jobTitle, countryName, jobDescription, joblocation, jobSalary,
            jobStatus
    ):
        try:
            countryId = JobDAO.get_country_dao(countryName)
            if not countryId:
                raise AppServices.handle_exception(
                    f"Country '{countryName}' not found.", is_raise=True
                )

            job_vo = JobVO()
            job_vo.jobCountryId = countryId
            job_vo.jobTitle = jobTitle
            job_vo.jobDescription = jobDescription
            job_vo.jobLocation = joblocation
            job_vo.jobSalary = jobSalary
            job_vo.jobStatus = jobStatus

            job_insert_data = JobDAO.insert_job_dao(job_vo)

            if not job_insert_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Inserted job: %s", job_vo.jobTitle)
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
    def get_all_job_service(pageNumber, pageSize, searchValue, sortBy, sortAs):
        try:
            result = JobDAO.get_all_job_dao(
                pageNumber=pageNumber,
                pageSize=pageSize,
                searchValue=searchValue,
                sortBy=sortBy,
                sortAs=sortAs,
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
    def delete_job_service(jobId):
        """Soft delete a job by ID."""
        try:
            delete_job_data = JobDAO.delete_job_dao(jobId)

            if not delete_job_data:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            delete_job_data.is_deleted = True  # Soft delete

            logger.info("Deleted job with ID: %s", jobId)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.DELETE_DATA.value,
                success=True,
                data=delete_job_data,
            )

        except Exception as exception:
            logger.exception("Error deleting job with ID: %s", jobId)
            return AppServices.handle_exception(exception)

    @staticmethod
    def get_job_by_id_service(jobId):
        """Retrieve job details for a given ID."""
        try:
            job_detail = JobDAO.get_job_by_id_dao(jobId)

            if not job_detail:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            logger.info("Fetched job detail for ID: %s", jobId)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.GET_DATA.value,
                success=True,
                data=job_detail,
            )

        except Exception as exception:
            logger.exception("Error retrieving job with ID: %s", jobId)
            return AppServices.handle_exception(exception)

    @staticmethod
    def update_job_service(
            jobId, jobTitle, countryName, jobDescription, jobLocation,
            jobSalary, jobStatus
    ):
        try:
            existing_job = JobDAO.get_job_by_id_dao(jobId)

            jobCountryId = JobDAO.get_country_dao(countryName)
            if not jobCountryId:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    f"Country '{countryName}' not found.",
                    success=False,
                    data={},
                )

            if not existing_job:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.NOT_FOUND.value,
                    success=False,
                    data={},
                )

            if jobTitle is not None:
                existing_job.jobTitle = jobTitle

            if jobCountryId is not None:
                existing_job.jobCountryId = jobCountryId

            if jobDescription is not None:
                existing_job.jobDescription = jobDescription

            if jobLocation is not None:
                existing_job.jobLocation = jobLocation

            if jobSalary is not None:
                existing_job.jobSalary = jobSalary

            if jobStatus is not None:
                existing_job.jobStatus = jobStatus

            # Step 3: Persist updated data
            updated_job = JobDAO.update_job_dao(existing_job)

            if not updated_job:
                return AppServices.app_response(
                    HttpStatusCodeEnum.BAD_REQUEST.value,
                    ResponseMessageEnum.UPDATE_FAILED.value,
                    success=False,
                    data={},
                )

            logger.info("Updated job with ID: %s", jobId)
            return AppServices.app_response(
                HttpStatusCodeEnum.ACCEPTED.value,
                ResponseMessageEnum.UPDATE_DATA.value,
                success=True,
                data=updated_job,
            )

        except Exception as exception:
            logger.exception("Error updating job")
            return AppServices.handle_exception(exception)
