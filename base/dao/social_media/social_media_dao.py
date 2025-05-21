from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.social_media_vo import SocialMediaVO


class SocialMediaDAO:

    @staticmethod
    def insert_social_media_dao(social_media_vo):
        """Call common insert method for social_media."""
        social_media_data = MysqlCommonQuery.insert_query(social_media_vo)
        return social_media_data

    @staticmethod
    def get_country_dao(country_name):
        social_media_country_id = MysqlCommonQuery.get_country_id_by_name(
            country_name)
        return social_media_country_id

    @staticmethod
    def get_all_social_media_dao(page_number, page_size, search_value, sort_by,
                                 sort_as):
        page_info = {
            "model": SocialMediaVO,
            "search_fields": ["social_media_title",
                              "social_media_description"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_social_media_dao(target_id):
        """Call common delete method for social_media."""
        social_media_data = MysqlCommonQuery.soft_delete_query(SocialMediaVO,
                                                               SocialMediaVO.social_media_id,
                                                               target_id)
        return social_media_data

    @staticmethod
    def get_social_media_by_id_dao(target_id):
        """Fetch a single social_media by ID (excluding soft-deleted
        records)."""
        social_media_data = MysqlCommonQuery.get_by_id_query(SocialMediaVO,
                                                             SocialMediaVO.social_media_id,
                                                             target_id)
        return social_media_data

    @staticmethod
    def update_social_media_dao(social_media_vo):
        """Update an existing social_media."""
        social_media_data = MysqlCommonQuery.update_query(social_media_vo)
        return social_media_data
