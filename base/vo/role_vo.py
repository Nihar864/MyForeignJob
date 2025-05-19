from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

from base.db.database import Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()
Base = declarative_base()


class RoleVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "role_table"
    __table_args__ = {"mysql_engine": "InnoDB"}
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)


Base.metadata.create_all(engine)
