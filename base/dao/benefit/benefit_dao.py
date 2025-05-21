from base.client.mysql_common.mysql_common_query import MysqlCommonQuery

QUERY = MysqlCommonQuery
from base.vo.benefit_vo import BenefitVO


class BenefitDAO:

    @staticmethod
    def check_existing_benefit(benefit_title):
        """Check if the benefit already exists."""
        get_data = MysqlCommonQuery.get_record_by_field(
            BenefitVO, "benefit_title", benefit_title
        )
        return get_data

    @staticmethod
    def insert_benefit_dao(benefit_vo):
        """Call common insert method for benefit."""
        benefit_data = MysqlCommonQuery.insert_query(benefit_vo)
        return benefit_data

    @staticmethod
    def get_all_benefit_dao(page_number, page_size, search_value, sort_by,
                            sort_as):
        page_info = {
            "model": BenefitVO,
            "search_fields": ["benefit_title", "benefit_description"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_benefit_dao(target_id):
        """Call common delete method for benefit."""
        benefit_data = QUERY.soft_delete_query(BenefitVO,
                                               BenefitVO.benefit_id,
                                               target_id)
        return benefit_data

    @staticmethod
    def get_benefit_by_id_dao(target_id):
        """Fetch a single benefit by ID (excluding soft-deleted records)."""
        benefit_data = MysqlCommonQuery.get_by_id_query(BenefitVO,
                                                        BenefitVO.benefit_id,
                                                        target_id)
        return benefit_data

    @staticmethod
    def update_benefit_dao(benefit_vo):
        """Update an existing benefit."""
        benefit_data = MysqlCommonQuery.update_query(benefit_vo)
        return benefit_data
