from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.country_vo import CountryVO


class CountryDAO:
    """
    Company Name : Softvan Pvt Ltd

    Purpose:
        Provide data access layer methods for Country entity operations.
    """

    @staticmethod
    def insert_country_dao(country_vo):
        """
        Request:
            country_vo: CountryVO instance representing the country to insert.

        Response:
            Returns the inserted CountryVO object with database state refreshed.

        Purpose:
            Insert a new country record into the database.

        Company Name : Softvan Pvt Ltd
        """
        country_data = MysqlCommonQuery.insert_query(country_vo)
        return country_data

    @staticmethod
    def get_all_categories_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request:
            page_number (int): Page number for pagination.
            page_size (int): Number of records per page.
            search_value (str): Search string to filter country_name field.
            sort_by (str): Field name to sort results.
            sort_as (str): Sort direction, 'asc' or 'desc'.

        Response:
            Returns dictionary with paginated list of CountryVO items and page metadata.

        Purpose:
            Retrieve all countries with optional filtering, sorting, and pagination.

        Company Name : Softvan Pvt Ltd
        """
        page_info = {
            "model": CountryVO,
            "search_fields": ["country_name"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_country_dao(target_id):
        """
        Request:
            target_id: Primary key (country_id) of the country to soft delete.

        Response:
            Returns the soft-deleted CountryVO object.

        Purpose:
            Soft delete a country record by setting its is_deleted flag.

        Company Name : Softvan Pvt Ltd
        """
        country_data = MysqlCommonQuery.soft_delete_query(
            CountryVO, CountryVO.country_id, target_id
        )
        return country_data

    @staticmethod
    def get_country_by_id_dao(target_id):
        """
        Request:
            target_id: Primary key (country_id) of the country to fetch.

        Response:
            Returns the CountryVO object if found and not soft deleted; else None.

        Purpose:
            Retrieve a single country record by its ID excluding soft-deleted entries.

        Company Name : Softvan Pvt Ltd
        """
        country_data = MysqlCommonQuery.get_by_id_query(
            CountryVO, CountryVO.country_id, target_id
        )
        return country_data

    @staticmethod
    def update_country_dao(country_vo):
        """
        Request:
            country_vo: CountryVO instance with updated data.

        Response:
            Returns the updated CountryVO object after committing changes.

        Purpose:
            Update an existing country record in the database.

        Company Name : Softvan Pvt Ltd
        """
        country_data = MysqlCommonQuery.update_query(country_vo)
        return country_data

    @staticmethod
    def check_existing_user(country_name):
        """
        Request:
            country_name (str): Name of the country to check for existence.

        Response:
            Returns CountryVO if a matching country is found; otherwise None.

        Purpose:
            Verify if a country with the given name already exists to prevent duplicates.

        Company Name : Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(
            CountryVO, "country_name", country_name
        )
        return get_data
