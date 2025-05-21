from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.news_vo import NewsVO


class NewsDAO:

    @staticmethod
    def insert_news_dao(news_vo):
        """Call common insert method for news."""
        news_data = MysqlCommonQuery.insert_query(news_vo)
        return news_data

    @staticmethod
    def get_country_dao(country_name):
        news_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return news_country_id

    @staticmethod
    def get_all_news_dao(page_number, page_size, search_value, sort_by,
                         sort_as):
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
        """Call common delete method for news."""
        news_data = MysqlCommonQuery.soft_delete_query(NewsVO, NewsVO.news_id,
                                                       target_id)
        return news_data

    @staticmethod
    def get_news_by_id_dao(target_id):
        """Fetch a single news by ID (excluding soft-deleted
        records)."""
        news_data = MysqlCommonQuery.get_by_id_query(NewsVO, NewsVO.news_id,
                                                     target_id)
        return news_data

    @staticmethod
    def update_news_dao(news_vo):
        """Update an existing news."""
        news_data = MysqlCommonQuery.update_query(news_vo)
        return news_data
