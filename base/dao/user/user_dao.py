from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.user_vo import UserVO


class UserDAO:
    """
    Company Name: Softvan Pvt Ltd

    Purpose:
        Data Access Object for CRUD operations related to User entity.
    """

    @staticmethod
    def check_existing_user_phone(phone_number):
        """
        Request:
            phone_number (str): Phone number to check for existence.

        Response:
            Returns UserVO instance if a user with the given phone exists, else None.

        Purpose:
            Verify if a user with the specified phone number already exists in the system.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(UserVO, "user_phone", phone_number)
        return get_data

    @staticmethod
    def check_existing_user_email(email):
        """
        Request:
            email (str): Email address to check for existence.

        Response:
            Returns UserVO instance if a user with the given email exists, else None.

        Purpose:
            Verify if a user with the specified email address already exists in the system.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(UserVO, "user_email", email)
        return get_data

    @staticmethod
    def insert_user_dao(user_vo):
        """
        Request:
            user_vo (UserVO): UserVO instance containing user details to insert.

        Response:
            Returns the inserted UserVO object with database-generated fields.

        Purpose:
            Insert a new user record into the database.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.insert_query(user_vo)
        return get_data

    @staticmethod
    def get_all_user_dao(page_number, page_size, search_value, sort_by, sort_as):
        """
        Request:
            page_number (int): The current page number for pagination.
            page_size (int): Number of records per page.
            search_value (str): Search term to filter users.
            sort_by (str): Field name to sort results by.
            sort_as (str): Sort order direction ('asc' or 'desc').

        Response:
            Returns a paginated list of UserVO objects matching search and sorting criteria.

        Purpose:
            Retrieve all user records with pagination, search, and sorting support.

        Company Name: Softvan Pvt Ltd
        """
        page_info = {
            "model": UserVO,
            "search_fields": ["user_name", "user_email", "user_phone", "user_country_name"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_user_dao(target_id):
        """
        Request:
            target_id (int): Unique identifier of the user to be soft deleted.

        Response:
            Returns the status/result of the soft delete operation.

        Purpose:
            Perform a soft delete on a user record, marking it inactive without physical deletion.

        Company Name: Softvan Pvt Ltd
        """
        user_data = MysqlCommonQuery.soft_delete_query(UserVO, UserVO.user_id, target_id)
        return user_data

    @staticmethod
    def get_user_by_id_dao(target_id):
        """
        Request:
            target_id (int): Unique identifier of the user.

        Response:
            Returns the UserVO object matching the provided ID, excluding soft-deleted users.

        Purpose:
            Fetch a single user record by ID for detailed view or update.

        Company Name: Softvan Pvt Ltd
        """
        user_data = MysqlCommonQuery.get_by_id_query(UserVO, UserVO.user_id, target_id)
        return user_data

    @staticmethod
    def update_user_dao(user_vo):
        """
        Request:
            user_vo (UserVO): UserVO instance containing updated user details.

        Response:
            Returns the updated UserVO object after successful commit.

        Purpose:
            Update an existing user record in the database.

        Company Name: Softvan Pvt Ltd
        """
        user_data = MysqlCommonQuery.update_query(user_vo)
        return user_data
