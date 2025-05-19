from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import AdminVO


class RegisterDAO:
    @staticmethod
    def check_existing_user(username):
        """Check if the username already exists."""
        get_data = MysqlCommonQuery.get_record_by_field(
            AdminVO, "login_username", username
        )
        return get_data

    @staticmethod
    def check_existing_phone(phone):
        """Check if the phone number already exists."""
        from base.vo.login_vo import AdminVO

        return MysqlCommonQuery.get_record_by_field(AdminVO, "login_phone", phone)

    @staticmethod
    def insert_register_user(register_vo):
        """Insert a new registered user."""
        get_data = MysqlCommonQuery.insert_query(register_vo)

        return get_data
