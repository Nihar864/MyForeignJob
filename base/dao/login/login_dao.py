"""
This module provides a set of data access methods for authentication and user management.
Author: Tarun Mondal
Designation: Software Engineer
"""

from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import AdminVO
from base.vo.role_vo import RoleVO


class AuthLoginDAO:

    @staticmethod
    def get_member_dao(m_id):
        get_data = MysqlCommonQuery.get_by_id_query(
            AdminVO,
            AdminVO.login_id,
        )
        return get_data

    @staticmethod
    def get_member_by_membership_id(membership_id):

        get_data = MysqlCommonQuery.get_by_membership_id(AdminVO, membership_id)
        print("2000",get_data)
        return get_data

    @staticmethod
    def get_role_by_id(role_id):
        return MysqlCommonQuery.get_role(RoleVO, RoleVO.role_id, role_id)

    @staticmethod
    def insert_login_user(login_vo):
        """Insert a new login user record."""
        get_data = MysqlCommonQuery.insert_query(login_vo)
        return get_data

    @staticmethod
    def get_admin_by_username(username):
        print("username",username)
        get_data = MysqlCommonQuery.get_record_by_field(
            AdminVO, "username", username
        )
        return get_data
