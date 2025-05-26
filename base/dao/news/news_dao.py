
from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.news_vo import NewsVO


class NewsDAO:
    """
    Company Name: Softvan Pvt Ltd

    Purpose:
        Data access object for CRUD operations related to News entity.
    """

    @staticmethod
    def insert_news_dao(news_vo):
        """
        Request:
            news_vo (NewsVO): NewsVO instance representing the news to insert.

        Response:
            Returns the inserted NewsVO object with updated database information.

        Purpose:
            Insert a new news record into the database.

        Company Name: Softvan Pvt Ltd
        """
        news_data = MysqlCommonQuery.insert_query(news_vo)
        return news_data

    @staticmethod
    def get_country_dao(country_name):
        """
        Request:
            country_name (str): Name of the country to fetch the corresponding ID.

        Response:
            Returns the country ID if the country exists, else None.

        Purpose:
            Retrieve the country ID based on the country name.

        Company Name: Softvan Pvt Ltd
        """
        news_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return news_country_id

    @staticmethod
    def get_all_news_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request:
            page_number (int): Current page number for pagination.
            page_size (int): Number of records per page.
            search_value (str): Search keyword to filter news records.
            sort_by (str): Column name to sort the results.
            sort_as (str): Sort order, 'asc' or 'desc'.

        Response:
            Returns a paginated list of NewsVO objects matching the search criteria and sorting.

        Purpose:
            Retrieve all news records with filtering, sorting, and pagination support.

        Company Name: Softvan Pvt Ltd
        """
        page_info = {
            "model": NewsVO,
            "search_fields": ["news_title", "news_description"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_news_dao(target_id):
        """
        Request:
            target_id (int): The unique ID of the news record to soft delete.

        Response:
            Returns the status/result of the soft delete operation.

        Purpose:
            Perform a soft delete on a news record by marking it as inactive/deleted.

        Company Name: Softvan Pvt Ltd
        """
        news_data = MysqlCommonQuery.soft_delete_query(NewsVO, NewsVO.news_id, target_id)
        return news_data

    @staticmethod
    def get_news_by_id_dao(target_id):
        """
        Request:
            target_id (int): The unique ID of the news record.

        Response:
            Returns the NewsVO object matching the ID if found, else None.

        Purpose:
            Fetch a single news record by its ID excluding soft-deleted entries.

        Company Name: Softvan Pvt Ltd
        """
        news_data = MysqlCommonQuery.get_by_id_query(NewsVO, NewsVO.news_id, target_id)
        return news_data

    @staticmethod
    def update_news_dao(news_vo):
        """
        Request:
            news_vo (NewsVO): NewsVO instance with updated information.

        Response:
            Returns the updated NewsVO object after committing changes.

        Purpose:
            Update an existing news record in the database.

        Company Name: Softvan Pvt Ltd
        """
        news_data = MysqlCommonQuery.update_query(news_vo)
        return news_data
