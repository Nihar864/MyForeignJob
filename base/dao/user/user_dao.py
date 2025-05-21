from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.user_vo import UserVO


class UserDAO:
    @staticmethod
    def check_existing_user_phone(phone_number):
        """Check if the phone already exists."""
        get_data = MysqlCommonQuery.get_record_by_field(
            UserVO, "user_phone", phone_number
        )
        return get_data

    @staticmethod
    def check_existing_user_email(email):
        """Check if the email already exists."""
        get_data = MysqlCommonQuery.get_record_by_field(
            UserVO, "user_email", email
        )
        return get_data

    @staticmethod
    def insert_user_dao(user_vo):
        """Insert a new user."""
        get_data = MysqlCommonQuery.insert_query(user_vo)

        return get_data

    @staticmethod
    def get_all_user_dao(page_number, page_size, search_value, sort_by,
                         sort_as):
        page_info = {
            "model": UserVO,
            "search_fields": ["user_name", "user_email", "user_phone",
                              "user_country_name"],
            "page_number": page_number,
            "page_size": page_size,
            "search_value": search_value,
            "sort_by": sort_by,
            "sort_as": sort_as,
        }
        return MysqlCommonQuery.get_all_with_filters(page_info)

    @staticmethod
    def delete_user_dao(target_id):
        """Call common delete method for user."""
        user_data = MysqlCommonQuery.soft_delete_query(UserVO, UserVO.user_id,
                                                       target_id)
        return user_data

    @staticmethod
    def get_user_by_id_dao(target_id):
        """Fetch a single user by ID (excluding soft-deleted records)."""
        user_data = MysqlCommonQuery.get_by_id_query(UserVO, UserVO.user_id,
                                                     target_id)
        return user_data

    @staticmethod
    def update_user_dao(user_vo):
        """Update an existing user."""
        user_data = MysqlCommonQuery.update_query(user_vo)
        return user_data
