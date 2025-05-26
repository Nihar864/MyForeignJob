from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.job_vo import JobVO


class JobDAO:
    """
    Company Name : Softvan Pvt Ltd

    Purpose:
        Data access object for managing Job entity CRUD operations.
    """

    @staticmethod
    def insert_job_dao(job_vo):
        """
        Request:
            job_vo: JobVO instance representing the job to insert.

        Response:
            Returns the inserted JobVO object with updated database state.

        Purpose:
            Insert a new job record into the database.

        Company Name : Softvan Pvt Ltd
        """
        job_data = MysqlCommonQuery.insert_query(job_vo)
        return job_data

    @staticmethod
    def get_all_job_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request:
            page_number (int): Page number for pagination.
            page_size (int): Number of job records per page.
            search_value (str): Search string to filter job title, description, or location.
            sort_by (str): Field to sort the results by.
            sort_as (str): Sort direction ('asc' or 'desc').

        Response:
            Returns a paginated list of jobs filtered and sorted based on parameters.

        Purpose:
            Fetch all jobs with support for search, sorting, and pagination.

        Company Name : Softvan Pvt Ltd
        """
        page_info = {
            "model": JobVO,
            "search_fields": ["job_title", "job_description", "job_location"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def get_country_dao(country_name):
        """
        Request:
            country_name (str): Name of the country to fetch ID for.

        Response:
            Returns the country_id corresponding to the country_name.

        Purpose:
            Retrieve the country ID by country name for job-country linkage.

        Company Name : Softvan Pvt Ltd
        """
        job_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return job_country_id

    @staticmethod
    def delete_job_dao(target_id):
        """
        Request:
            target_id: Primary key (job_id) of the job to soft delete.

        Response:
            Returns the soft-deleted JobVO object.

        Purpose:
            Soft delete a job by marking it as deleted without physical removal.

        Company Name : Softvan Pvt Ltd
        """
        job_data = MysqlCommonQuery.soft_delete_query(JobVO, JobVO.job_id, target_id)
        return job_data

    @staticmethod
    def get_job_by_id_dao(target_id):
        """
        Request:
            target_id: Primary key (job_id) of the job to fetch.

        Response:
            Returns the JobVO object if found and not soft deleted; otherwise None.

        Purpose:
            Retrieve a specific job by ID excluding soft-deleted entries.

        Company Name : Softvan Pvt Ltd
        """
        job_data = MysqlCommonQuery.get_by_id_query(JobVO, JobVO.job_id, target_id)
        return job_data

    @staticmethod
    def update_job_dao(job_vo):
        """
        Request:
            job_vo: JobVO instance with updated job data.

        Response:
            Returns the updated JobVO object after committing the update.

        Purpose:
            Update an existing job record in the database.

        Company Name : Softvan Pvt Ltd
        """
        job_data = MysqlCommonQuery.update_query(job_vo)
        return job_data
