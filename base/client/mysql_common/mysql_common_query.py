from sqlalchemy import or_, asc, desc
from sqlalchemy.exc import SQLAlchemyError

from base.db.database import Database
from base.vo.country_vo import CountryVO

database = Database()
engine = database.get_db_connection()


class MysqlCommonQuery:
    """Generic MySQL repository for common database operations."""

    @staticmethod
    def insert_query(create_object):
        session = database.get_db_session(engine)
        try:
            session.add(create_object)
            session.commit()
            session.refresh(create_object)
            return create_object
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @staticmethod
    def get_all_query(table_name):
        """Retrieve all non-deleted entities of a given model."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name).filter(table_name.is_deleted == False).all()
        )
        return table_data

    @staticmethod
    def soft_delete_query(table_name, table_id, entity_id):
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name)
            .filter(table_id == entity_id, table_name.is_deleted == False)
            .first()
        )
        table_data.is_deleted = True
        session.commit()
        return table_data

    @staticmethod
    def get_by_id_query(table_name, table_id, entity_id):
        """Retrieve an entity by its ID, excluding soft-deleted entities."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name)
            .filter(table_id == entity_id, table_name.is_deleted == False)
            .first()
        )
        return table_data

    @staticmethod
    def update_query(update_record):
        """Commit updates to an existing entity."""
        session = database.get_db_session(engine)
        session.merge(update_record)
        session.flush()
        session.commit()
        session.close()
        return update_record

    @staticmethod
    def get_record_by_field(model, field_name, value):
        session = database.get_db_session(engine)
        user_data = (
            session.query(model).filter(getattr(model, field_name) == value).first()
        )
        session.close()
        return user_data

    @staticmethod
    def update_login_status(
        model_class, table_id, model_id, current_login_status: bool
    ):
        session = database.get_db_session(engine)

        existing_user = session.query(model_class).filter(table_id == model_id).first()

        if existing_user:
            existing_user.login_status = current_login_status
            session.commit()

        session.close()
        return existing_user

    @staticmethod
    def get_all_with_filters(page_info):
        session = database.get_db_session(engine)

        model = page_info["model"]
        search_fields = page_info.get("search_fields", [])
        search_value = page_info.get("search_value", "")
        page_number = page_info.get("page_number", 1)
        page_size = page_info.get("page_size", 10)
        sort_by = page_info.get("sort_by", "id")
        sort_as = page_info.get("sort_as", "asc")

        query = session.query(model).filter(model.is_deleted == False)

        if search_value and search_fields:
            search_term = f"%{search_value.lower()}%"
            query = query.filter(
                or_(
                    *[
                        getattr(model, field).ilike(search_term)
                        for field in search_fields
                    ]
                )
            )

        if hasattr(model, sort_by):
            sort_column = getattr(model, sort_by)
            query = query.order_by(
                asc(sort_column) if sort_as == "asc" else desc(sort_column)
            )
        else:
            query = query.order_by(model.id.asc())

        total = query.count()
        offset = (page_number - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        session.close()

        return {
            "items": items,
            "page_info": {"total": total, "page": page_number, "limit": page_size},
        }

    @staticmethod
    def fetch_email_by_login_username(register_vo, login_vo, username, loginId):
        session = database.get_db_session(engine)
        result = (
            session.query(register_vo.register_email)
            .join(login_vo, register_vo.register_login_vo == loginId)
            .filter(login_vo.login_username == username)
            .first()
        )
        print(f"result{result}")
        return result

    @staticmethod
    def get_country_id_by_name(name: str):
        session = database.get_db_session(engine)
        try:
            country = (
                session.query(CountryVO).filter(CountryVO.country_name == name).first()
            )
            return country.country_id if country else None
        finally:
            session.close()

    @staticmethod
    def get_role(table, pk_column, value):
        session = database.get_db_session(engine)
        result = session.query(table).filter(pk_column == value).first()
        return result

    @staticmethod
    def get_by_membership_id(table_name, membership_id):
        """
        Retrieve a database record by membership ID.
        Author: Tarun Mondal
        Designation: Software Engineer

        Args:
            table_name: The table representing the database entity.
            membership_id: The membership ID to search for.

        Returns:
            The retrieved database record or None if not found.
        """
        session = database.get_db_session(engine)
        db_data = session.query(table_name).filter_by(membership_id=membership_id).first()

        return db_data
