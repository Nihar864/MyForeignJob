from sqlalchemy import or_, asc, desc

from base.db.database import Database
from base.vo.country_vo import CountryVO

database = Database()
engine = database.get_db_connection()


class MysqlCommonQuery:
    """Generic MySQL repository for common database operations."""

    @staticmethod
    def insert_query(create_object):
        """Insert a new entity into the database."""
        session = database.get_db_session(engine)
        session.add(create_object)
        session.commit()
        session.refresh(create_object)
        return create_object

    @staticmethod
    def get_all_query(table_name):
        """Retrieve all non-deleted entities of a given model."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name).filter(
                table_name.isDeleted == False).all()
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

    # #
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
            session.query(model).filter(
                getattr(model, field_name) == value).first()
        )
        session.close()
        return user_data

    @staticmethod
    def update_login_status(
            model_class, table_id, model_id, current_login_status: bool
    ):
        session = database.get_db_session(engine)

        existing_user = session.query(model_class).filter(
            table_id == model_id).first()

        if existing_user:
            existing_user.login_status = current_login_status
            session.commit()

        session.close()
        return existing_user

    @staticmethod
    def get_all_with_filters(
            model,
            search_fields,
            page_number, page_size, search_value, sort_by,
            sort_as
    ):
        session = database.get_db_session(engine)

        query = session.query(model).filter(model.is_deleted == False)

        # Searching (if any field matches search_term)
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

        # Sorting
        if hasattr(model, sort_by):
            sort_column = getattr(model, sort_by)
            query = query.order_by(
                asc(sort_column) if sort_as == "asc" else desc(sort_column)
            )
        else:
            query = query.order_by(model.id.asc())  # fallback

        # Pagination
        total = query.count()
        offset = (page_number - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        session.close()

        return {"items": items, "total": total, "page": page_number,
                "limit": page_size}

    @staticmethod
    def update_user_password_by_username(model, username, new_password):
        session = database.get_db_session(engine)
        user = session.query(model).filter(
            model.loginUsername == username).first()
        user.login_password = new_password
        session.commit()
        return True

    @staticmethod
    def fetch_email_by_login_username(register_vo, login_vo, username,
                                      loginId):
        session = database.get_db_session(engine)
        result = (
            session.query(register_vo.register_email)
            .join(login_vo, register_vo.register_login_vo == loginId)
            .filter(login_vo.loginUsername == username)
            .first()
        )
        print(f"result{result}")
        return result

    @staticmethod
    def get_country_id_by_name(name: str):
        session = database.get_db_session(engine)
        try:
            country = (
                session.query(CountryVO).filter(
                    CountryVO.country_name == name).first()
            )
            return country.country_id if country else None
        finally:
            session.close()
