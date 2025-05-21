from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.rules_vo import RuleVO


class RuleDAO:

    @staticmethod
    def insert_rule_dao(rule_vo):
        """Call common insert method for rule."""
        rule_data = MysqlCommonQuery.insert_query(rule_vo)
        return rule_data

    @staticmethod
    def get_country_dao(country_name):
        rule_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return rule_country_id

    @staticmethod
    def get_all_rule_dao(page_number, page_size, search_value, sort_by,
                         sort_as):
        page_info = {
            "model": RuleVO,
            "search_fields": ["rule_title", "rule_description"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_rule_dao(target_id):
        """Call common delete method for rule."""
        rule_data = MysqlCommonQuery.soft_delete_query(RuleVO, RuleVO.rule_id,
                                                       target_id)
        return rule_data

    @staticmethod
    def get_rule_by_id_dao(target_id):
        """Fetch a single rule by ID (excluding soft-deleted records)."""
        rule_data = MysqlCommonQuery.get_by_id_query(RuleVO, RuleVO.rule_id,
                                                     target_id)
        return rule_data

    @staticmethod
    def update_rule_dao(rule_vo):
        """Update an existing rule."""
        rule_data = MysqlCommonQuery.update_query(rule_vo)
        return rule_data
