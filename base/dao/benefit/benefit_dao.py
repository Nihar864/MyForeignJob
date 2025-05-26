from base.client.mysql_common.mysql_common_query import MysqlCommonQuery

QUERY = MysqlCommonQuery
from base.vo.benefit_vo import BenefitVO


class BenefitDAO:

    @staticmethod
    def check_existing_benefit(benefit_title):
        """
        Check if a benefit with the given title already exists.

        Request:
            - benefit_title (str): The title to check for existing benefits

        Response:
            - BenefitVO object if benefit exists
            - None if no matching benefit found

        Purpose:
            - Prevent duplicate benefit entries
            - Validate uniqueness of benefit titles

        Company Name:
            - Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(
            BenefitVO, "benefit_title", benefit_title
        )
        return get_data

    @staticmethod
    def insert_benefit_dao(benefit_vo):
        """
        Insert a new benefit record into the database.

        Request:
            - benefit_vo (BenefitVO): Benefit value object containing all required fields

        Response:
            - Inserted BenefitVO object with generated ID
            - None if insertion failed

        Purpose:
            - Persist new benefit data to database
            - Return complete benefit record including generated ID

        Company Name:
            - Softvan Pvt Ltd
        """
        benefit_data = MysqlCommonQuery.insert_query(benefit_vo)
        return benefit_data

    @staticmethod
    def get_all_benefit_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Retrieve paginated list of benefits with filtering and sorting options.

        Request:
            - page_number (int): Current page number for pagination
            - page_size (int): Number of items per page
            - search_value (str): Value to search in benefit fields
            - sort_by (str): Field name to sort by
            - sort_as (str): Sorting direction ('asc' or 'desc')

        Response:
            - Dictionary containing:
                - items: List of BenefitVO objects
                - total: Total count of matching records
                - pages: Total number of pages

        Purpose:
            - Provide filtered, sorted and paginated benefit data
            - Support data tables and grid views in UI

        Company Name:
            - Softvan Pvt Ltd
        """
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
        """
        Soft delete a benefit record by ID.

        Request:
            - target_id (int): ID of the benefit to be deleted

        Response:
            - Updated BenefitVO object with is_deleted=True
            - None if record not found

        Purpose:
            - Mark benefit as deleted without physical removal
            - Maintain referential integrity
            - Allow potential recovery of deleted items

        Company Name:
            - Softvan Pvt Ltd
        """
        benefit_data = QUERY.soft_delete_query(
            BenefitVO, BenefitVO.benefit_id, target_id
        )
        return benefit_data

    @staticmethod
    def get_benefit_by_id_dao(target_id):
        """
        Retrieve a single benefit record by its ID.

        Request:
            - target_id (int): ID of the benefit to retrieve

        Response:
            - BenefitVO object if found
            - None if no matching record found

        Purpose:
            - Get complete details of a specific benefit
            - Support edit/view operations
            - Exclude soft-deleted records

        Company Name:
            - Softvan Pvt Ltd
        """
        benefit_data = MysqlCommonQuery.get_by_id_query(
            BenefitVO, BenefitVO.benefit_id, target_id
        )
        return benefit_data

    @staticmethod
    def update_benefit_dao(benefit_vo):
        """
        Update an existing benefit record.

        Request:
            - benefit_vo (BenefitVO): Benefit value object with updated fields

        Response:
            - Updated BenefitVO object
            - None if update failed

        Purpose:
            - Persist changes to benefit data
            - Maintain data consistency
            - Return complete updated record

        Company Name:
            - Softvan Pvt Ltd
        """
        benefit_data = MysqlCommonQuery.update_query(benefit_vo)
        return benefit_data
