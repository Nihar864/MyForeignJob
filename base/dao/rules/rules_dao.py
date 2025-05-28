from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.rules_vo import RuleVO


class RuleDAO:
    """
    Company Name: Softvan Pvt Ltd

    Purpose:
        Data access object for CRUD operations related to Rule entity.
    """

    @staticmethod
    def insert_rule_dao(rule_vo):
        """
        Request:
            rule_vo (RuleVO): RuleVO instance representing the rule to insert.

        Response:
            Returns the inserted RuleVO object with updated database information.

        Purpose:
            Insert a new rule record into the database.

        Company Name: Softvan Pvt Ltd
        """
        rule_data = MysqlCommonQuery.insert_query(rule_vo)
        return rule_data

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
        rule_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return rule_country_id

    @staticmethod
    def get_all_rule_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request:
            page_number (int): Current page number for pagination.
            page_size (int): Number of records per page.
            search_value (str): Search keyword to filter rule records.
            sort_by (str): Column name to sort the results.
            sort_as (str): Sort order, 'asc' or 'desc'.

        Response:
            Returns a paginated list of RuleVO objects matching the search criteria and sorting.

        Purpose:
            Retrieve all rule records with filtering, sorting, and pagination support.

        Company Name: Softvan Pvt Ltd
        """
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
        """
        Request:
            target_id (int): The unique ID of the rule record to soft delete.

        Response:
            Returns the status/result of the soft delete operation.

        Purpose:
            Perform a soft delete on a rule record by marking it as inactive/deleted.

        Company Name: Softvan Pvt Ltd
        """
        rule_data = MysqlCommonQuery.soft_delete_query(
            RuleVO, RuleVO.rule_id, target_id
        )
        return rule_data

    @staticmethod
    def get_rule_by_id_dao(target_id):
        """
        Request:
            target_id (int): The unique ID of the rule record.

        Response:
            Returns the RuleVO object matching the ID if found, else None.

        Purpose:
            Fetch a single rule record by its ID excluding soft-deleted entries.

        Company Name: Softvan Pvt Ltd
        """
        rule_data = MysqlCommonQuery.get_by_id_query(RuleVO, RuleVO.rule_id, target_id)
        return rule_data

    @staticmethod
    def update_rule_dao(rule_vo):
        """
        Request:
            rule_vo (RuleVO): RuleVO instance with updated information.

        Response:
            Returns the updated RuleVO object after committing changes.

        Purpose:
            Update an existing rule record in the database.

        Company Name: Softvan Pvt Ltd
        """
        rule_data = MysqlCommonQuery.update_query(rule_vo)
        return rule_data

    @staticmethod
    def check_existing_rule(rule_title):
        """
        Check if a rule with the given title already exists.

        Request:
            - rule_title (str): The title to check for existing rules

        Response:
            - ruleVO object if rule exists
            - None if no matching rule found

        Purpose:
            - Prevent duplicate rule entries
            - Validate uniqueness of rule titles

        Company Name:
            - Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(
            RuleVO, "rule_title", rule_title
        )
        return get_data
