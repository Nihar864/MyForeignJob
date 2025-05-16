from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.faq_vo import FaqVO


class FaqDAO:

    @staticmethod
    def insert_faq_dao(faq_vo):
        """Call common insert method for faq."""
        faq_data = MysqlCommonQuery.insert_query(faq_vo)
        return faq_data

    @staticmethod
    def get_country_dao(country_name):
        faq_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return faq_country_id

    @staticmethod
    def get_all_faq_dao(page_number, page_size, search_value, sort_by,
                        sort_as):
        page_info = {
            "model": FaqVO,
            "search_fields": ["faq_title", "faq_description"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_faq_dao(target_id):
        """Call common delete method for faq."""
        faq_data = MysqlCommonQuery.soft_delete_query(FaqVO, FaqVO.faq_id,
                                                      target_id)
        return faq_data

    @staticmethod
    def get_faq_by_id_dao(target_id):
        """Fetch a single faq by ID (excluding soft-deleted records)."""
        faq_data = MysqlCommonQuery.get_by_id_query(FaqVO, FaqVO.faq_id,
                                                    target_id)
        return faq_data

    @staticmethod
    def update_faq_dao(faq_vo):
        """Update an existing faq."""
        faq_data = MysqlCommonQuery.update_query(faq_vo)

        return faq_data