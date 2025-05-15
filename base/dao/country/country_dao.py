from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.country_vo import CountryVO


class CountryDAO:
    @staticmethod
    def insert_country_dao(country_vo):
        """Call common insert method for country."""
        country_data = MysqlCommonQuery.insert_query(country_vo)
        return country_data

    @staticmethod
    def get_all_categories_dao(pageNumber, pageSize, searchValue, sortBy, sortAs):

        return MysqlCommonQuery.get_all_with_filters(
            model=CountryVO,
            searchFields=["countryName"],
            searchValue=searchValue,
            pageNumber=pageNumber,
            pageSize=pageSize,
            sortBy=sortBy,
            sortAs=sortAs,
        )

    @staticmethod
    def delete_country_dao(target_id):
        """Call common delete method for country."""
        country_data = MysqlCommonQuery.soft_delete_query(
            CountryVO, CountryVO.countryId, target_id
        )
        return country_data

    @staticmethod
    def get_country_by_id_dao(target_id):
        """Fetch a single country by ID (excluding soft-deleted records)."""
        country_data = MysqlCommonQuery.get_by_id_query(
            CountryVO, CountryVO.countryId, target_id
        )
        return country_data

    @staticmethod
    def update_country_dao(country_vo):
        """Update an existing country."""
        country_data = MysqlCommonQuery.update_query(country_vo)
        return country_data
