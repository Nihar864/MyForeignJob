from sqlalchemy import Column, Integer, String, ForeignKey
from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class RegisterVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "register_table"

    registerId = Column(Integer, primary_key=True, index=True)

    registerName = Column(String(50), nullable=False)

    registerEmail = Column(String(100), nullable=False, unique=True)

    registerPhone = Column(String(15), nullable=False, unique=True)


Base.metadata.create_all(engine)
