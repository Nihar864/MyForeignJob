from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from base.db.database import Database
from base.vo.role_vo import RoleVO

from base.mixins import StatusMixin, TimestampMixin

# Create a database connection
database = Database()
engine = database.get_db_connection()
Base = declarative_base()


class AdminVO(Base, StatusMixin, TimestampMixin):

    __tablename__ = "admin_table"
    __table_args__ = {"mysql_engine": "InnoDB"}
    login_id = Column(Integer, primary_key=True)
    username = Column(String(500), nullable=False)
    password = Column(String(500), nullable=False)
    role = Column(
        Integer, ForeignKey(RoleVO.role_id, ondelete="CASCADE", onupdate="CASCADE")
    )

    @staticmethod
    def serialize(data):

        return {
            "admin_id": data.login_id,
            "username": data.username,
        }


# Create the table in the database
Base.metadata.create_all(engine)
