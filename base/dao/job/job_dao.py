from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.job_vo import JobVO


class JobDAO:

    @staticmethod
    def insert_job_dao(jobvo):
        """Call common insert method for job."""
        job_data = MysqlCommonQuery.insert_query(jobvo)
        return job_data

    @staticmethod
    def get_all_job_dao(pageNumber, pageSize, searchValue, sortBy, sortAs):
        return MysqlCommonQuery.get_all_with_filters(
            model=JobVO,
            searchFields=["jobTitle", "jobDescription", "jobLocation"],
            searchValue=searchValue,
            pageNumber=pageNumber,
            pageSize=pageSize,
            sortBy=sortBy,
            sortAs=sortAs,
        )

    @staticmethod
    def get_country_dao(countryName):
        jobCountryId = MysqlCommonQuery.get_country_id_by_name(countryName)
        return jobCountryId

    @staticmethod
    def delete_job_dao(target_id):
        """Call common delete method for job."""
        job_data = MysqlCommonQuery.soft_delete_query(JobVO, JobVO.jobId, target_id)
        return job_data

    @staticmethod
    def get_job_by_id_dao(target_id):
        """Fetch a single job by ID (excluding soft-deleted records)."""
        job_data = MysqlCommonQuery.get_by_id_query(JobVO, JobVO.jobId, target_id)
        return job_data

    @staticmethod
    def update_job_dao(job_vo):
        """Update an existing job."""
        job_data = MysqlCommonQuery.update_query(job_vo)

        return job_data
