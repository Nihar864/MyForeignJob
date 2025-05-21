from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class NewsVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "news_table"

    news_id = Column(Integer, primary_key=True, index=True)
    news_title = Column(String(500), unique=True, index=True,
                        nullable=False)
    news_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", ondelete="CASCADE",
                   onupdate="CASCADE"),
        nullable=False, )
    news_country_name = Column(String(50), nullable=False)
    news_description = Column(String(500), nullable=False)
    news_url = Column(String(500), nullable=False)
    news_status = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(engine)
