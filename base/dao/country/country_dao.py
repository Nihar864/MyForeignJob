from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.country_vo import CountryVO


class CountryDAO:
    @staticmethod
    def insert_country_dao(country_vo):
        """Call common insert method for country."""
        country_data = MysqlCommonQuery.insert_query(country_vo)
        return country_data

    @staticmethod
    def get_all_categories_dao(page_number, page_size, search_value, sort_by, sort_as):
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
        """Call common delete method for country."""
        country_data = MysqlCommonQuery.soft_delete_query(
            CountryVO, CountryVO.country_id, target_id
        )
        return country_data

    @staticmethod
    def get_country_by_id_dao(target_id):
        """Fetch a single country by ID (excluding soft-deleted records)."""
        country_data = MysqlCommonQuery.get_by_id_query(
            CountryVO, CountryVO.country_id, target_id
        )
        return country_data

    @staticmethod
    def update_country_dao(country_vo):
        """Update an existing country."""
        country_data = MysqlCommonQuery.update_query(country_vo)
        return country_data

    @staticmethod
    def check_existing_user(country_name):
        """Check if the username already exists."""
        get_data = MysqlCommonQuery.get_record_by_field(
            CountryVO, "country_name", country_name
        )
        return get_data
