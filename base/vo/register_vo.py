from sqlalchemy import Column, Integer, String

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class RegisterVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "register_table"

    register_id = Column(Integer, primary_key=True, index=True)

    register_name = Column(String(50), nullable=False)

    register_email = Column(String(100), nullable=False, unique=True)

    register_phone = Column(String(15), nullable=False, unique=True)


# Base.metadata.create_all(engine)
