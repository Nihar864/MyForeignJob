from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.social_media_vo import SocialMediaVO


class SocialMediaDAO:
    """
    Company Name: Softvan Pvt Ltd

    Purpose:
        Data access object for CRUD operations related to Social Media entity.
    """

    @staticmethod
    def insert_social_media_dao(social_media_vo):
        """
        Request:
            social_media_vo (SocialMediaVO): Instance representing the social media record to insert.

        Response:
            Returns the inserted SocialMediaVO object with database-assigned attributes.

        Purpose:
            Insert a new social media record into the database.

        Company Name: Softvan Pvt Ltd
        """
        social_media_data = MysqlCommonQuery.insert_query(social_media_vo)
        return social_media_data

    @staticmethod
    def get_country_dao(country_name):
        """
        Request:
            country_name (str): The name of the country to find the corresponding ID.

        Response:
            Returns the country ID matching the provided country name.

        Purpose:
            Retrieve the country ID based on the country name for association.

        Company Name: Softvan Pvt Ltd
        """
        social_media_country_id = MysqlCommonQuery.get_country_id_by_name(country_name)
        return social_media_country_id

    @staticmethod
    def get_all_social_media_dao(
        page_number, page_size, search_value, sort_by, sort_as
    ):
        """
        Request:
            page_number (int): Pagination page number.
            page_size (int): Number of records per page.
            search_value (str): Search keyword for filtering records.
            sort_by (str): Field name to sort results by.
            sort_as (str): Sort order ('asc' or 'desc').

        Response:
            Returns a paginated, filtered, and sorted list of SocialMediaVO records.

        Purpose:
            Retrieve all social media records with support for search, sorting, and pagination.

        Company Name: Softvan Pvt Ltd
        """
        page_info = {
            "model": SocialMediaVO,
            "search_fields": ["social_media_title", "social_media_description"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_social_media_dao(target_id):
        """
        Request:
            target_id (int): ID of the social media record to soft delete.

        Response:
            Returns the status/result of the soft delete operation.

        Purpose:
            Soft delete a social media record by marking it inactive without physical deletion.

        Company Name: Softvan Pvt Ltd
        """
        social_media_data = MysqlCommonQuery.soft_delete_query(
            SocialMediaVO, SocialMediaVO.social_media_id, target_id
        )
        return social_media_data

    @staticmethod
    def get_social_media_by_id_dao(target_id):
        """
        Request:
            target_id (int): Unique ID of the social media record.

        Response:
            Returns the SocialMediaVO object matching the ID, excluding soft-deleted records.

        Purpose:
            Fetch a single social media record by its unique ID.

        Company Name: Softvan Pvt Ltd
        """
        social_media_data = MysqlCommonQuery.get_by_id_query(
            SocialMediaVO, SocialMediaVO.social_media_id, target_id
        )
        return social_media_data

    @staticmethod
    def update_social_media_dao(social_media_vo):
        """
        Request:
            social_media_vo (SocialMediaVO): SocialMediaVO instance containing updated data.

        Response:
            Returns the updated SocialMediaVO object after successful update.

        Purpose:
            Update an existing social media record in the database.

        Company Name: Softvan Pvt Ltd
        """
        social_media_data = MysqlCommonQuery.update_query(social_media_vo)
        return social_media_data

    @staticmethod
    def check_existing_social_media(social_media_title):
        """
        Check if a social_media with the given title already exists.

        Request:
            - social_media_title (str): The title to check for existing social_medias

        Response:
            - social_mediaVO object if social_media exists
            - None if no matching social_media found

        Purpose:
            - Prevent duplicate social_media entries
            - Validate uniqueness of social_media titles

        Company Name:
            - Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(
            SocialMediaVO, "social_media_title", social_media_title
        )
        return get_data
