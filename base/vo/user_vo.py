from sqlalchemy import Column, Integer, String, ForeignKey

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class UserVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True, index=True)

    user_name = Column(String(50), nullable=False)

    user_email = Column(String(100), nullable=False, unique=True)

    user_phone = Column(String(15), nullable=False, unique=True)

    user_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", ondelete="CASCADE",
                   onupdate="CASCADE"),
        nullable=False, )

    user_country_name = Column(String(50), nullable=False)


Base.metadata.create_all(engine)
