from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.db.database import Database
from base.vo.login_vo import LoginVO
from base.vo.register_vo import RegisterVO

database = Database()
engine = database.get_db_connection()


class LoginDAO:
    @staticmethod
    def insert_login_user(login_vo):
        """Insert a new login user record."""
        get_data = MysqlCommonQuery.insert_query(login_vo)
        return get_data

    @staticmethod
    def get_user_by_username(username):
        get_data = MysqlCommonQuery.get_record_by_field(
            LoginVO, "login_username", username
        )
        print("get_user_by_username", get_data.__dict__)
        return get_data

    @staticmethod
    def update_login_status(user, current_login_status):
        updated_user = MysqlCommonQuery.update_login_status(
            LoginVO, LoginVO.loginId, user.loginId, current_login_status
        )
        return updated_user

    @staticmethod
    def get_user_email_by_username(username: str):
        get_data = MysqlCommonQuery.fetch_email_by_login_username(
            RegisterVO, LoginVO, username, LoginVO.loginId
        )
        return get_data[0]

    @staticmethod
    def update_user_password_by_username(username: str, new_password: str):
        get_data = MysqlCommonQuery.update_user_password_by_username(
            LoginVO, username, new_password
        )
        return get_data
