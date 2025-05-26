from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.faq_vo import FaqVO


class FaqDAO:
    """
    Company Name : Softvan Pvt Ltd

    Purpose:
        Data access object for managing FAQ entity CRUD operations.
    """

    @staticmethod
    def insert_faq_dao(faq_vo):
        """
        Request:
            faq_vo: FaqVO instance representing the FAQ to insert.

        Response:
            Returns the inserted FaqVO object with updated database state.

        Purpose:
            Insert a new FAQ record into the database.

        Company Name : Softvan Pvt Ltd
        """
        faq_data = MysqlCommonQuery.insert_query(faq_vo)
        return faq_data

    @staticmethod
    def get_country_dao(country_name):
        """
        Request:
            country_name (str): Name of the country for which to fetch the ID.

        Response:
            Returns the country_id corresponding to the country_name if found.

        Purpose:
            Retrieve the country ID by country name, used for FAQ linkage.

        Company Name : Softvan Pvt Ltd
        """
        faq_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return faq_country_id

    @staticmethod
    def get_all_faq_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request:
            page_number (int): Page number for pagination.
            page_size (int): Number of FAQs per page.
            search_value (str): Search string to filter FAQ title or description.
            sort_by (str): Field to sort the results by.
            sort_as (str): Sort direction ('asc' or 'desc').

        Response:
            Returns a paginated list of FAQs with applied filters and sorting.

        Purpose:
            Fetch all FAQs with support for search, sorting, and pagination.

        Company Name : Softvan Pvt Ltd
        """
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
        """
        Request:
            target_id: Primary key (faq_id) of the FAQ to soft delete.

        Response:
            Returns the soft-deleted FaqVO object.

        Purpose:
            Soft delete an FAQ by marking it as deleted without physical removal.

        Company Name : Softvan Pvt Ltd
        """
        faq_data = MysqlCommonQuery.soft_delete_query(FaqVO, FaqVO.faq_id, target_id)
        return faq_data

    @staticmethod
    def get_faq_by_id_dao(target_id):
        """
        Request:
            target_id: Primary key (faq_id) of the FAQ to fetch.

        Response:
            Returns the FaqVO object if found and not soft deleted; otherwise None.

        Purpose:
            Retrieve a specific FAQ by ID excluding soft-deleted entries.

        Company Name : Softvan Pvt Ltd
        """
        faq_data = MysqlCommonQuery.get_by_id_query(FaqVO, FaqVO.faq_id, target_id)
        return faq_data

    @staticmethod
    def update_faq_dao(faq_vo):
        """
        Request:
            faq_vo: FaqVO instance with updated FAQ data.

        Response:
            Returns the updated FaqVO object after committing the update.

        Purpose:
            Update an existing FAQ record in the database.

        Company Name : Softvan Pvt Ltd
        """
        faq_data = MysqlCommonQuery.update_query(faq_vo)
        return faq_data
