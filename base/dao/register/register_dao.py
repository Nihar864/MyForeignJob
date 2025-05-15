from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import LoginVO


class RegisterDAO:
    @staticmethod
    def check_existing_user(username):
        """Check if the username already exists."""
        get_data = MysqlCommonQuery.get_record_by_field(
            LoginVO, "loginUsername", username
        )
        return get_data

    @staticmethod
    def insert_register_user(register_vo):
        """Insert a new registered user."""
        get_data = MysqlCommonQuery.insert_query(register_vo)

        return get_data
