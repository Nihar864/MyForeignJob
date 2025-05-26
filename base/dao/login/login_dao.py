from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import AdminVO
from base.vo.role_vo import RoleVO


class AuthLoginDAO:
    """
    Company Name: Softvan Pvt Ltd

    Purpose:
        Data access object for authentication and user management operations.
    """

    @staticmethod
    def get_member_dao(m_id):
        """
        Request:
            m_id (int): The unique login ID of the member.

        Response:
            Returns the AdminVO object matching the login ID if found, else None.

        Purpose:
            Retrieve a member record by its unique login ID.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_by_id_query(AdminVO, AdminVO.login_id, m_id)
        return get_data

    @staticmethod
    def get_member_by_membership_id(membership_id):
        """
        Request:
            membership_id (str): The unique membership ID of the member.

        Response:
            Returns the AdminVO object matching the membership ID if found, else None.

        Purpose:
            Retrieve a member record by its membership ID.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_by_membership_id(AdminVO, membership_id)
        return get_data

    @staticmethod
    def get_role_by_id(role_id):
        """
        Request:
            role_id (int): The unique role ID.

        Response:
            Returns the RoleVO object matching the role ID if found, else None.

        Purpose:
            Retrieve a role record by its unique role ID.

        Company Name: Softvan Pvt Ltd
        """
        return MysqlCommonQuery.get_role(RoleVO, RoleVO.role_id, role_id)

    @staticmethod
    def insert_login_user(login_vo):
        """
        Request:
            login_vo (AdminVO): The AdminVO instance representing the new login user.

        Response:
            Returns the inserted AdminVO object with updated database state.

        Purpose:
            Insert a new login user record into the database.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.insert_query(login_vo)
        return get_data

    @staticmethod
    def get_admin_by_username(username):
        """
        Request:
            username (str): The username of the admin user.

        Response:
            Returns the AdminVO object matching the username if found, else None.

        Purpose:
            Retrieve an admin user by their username.

        Company Name: Softvan Pvt Ltd
        """
        get_data = MysqlCommonQuery.get_record_by_field(AdminVO, "username", username)
        return get_data

    @staticmethod
    def update_password_dao(login_vo):
        """
        Request:
            login_vo (AdminVO): The AdminVO instance containing updated password information.

        Response:
            Returns the updated AdminVO object after committing the password update.

        Purpose:
            Update the password for an existing login user.

        Company Name: Softvan Pvt Ltd
        """
        user_data = MysqlCommonQuery.update_query(login_vo)
        return user_data

