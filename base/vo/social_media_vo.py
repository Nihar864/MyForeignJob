from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class SocialMediaVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "social_media_table"

    social_media_id = Column(Integer, primary_key=True, index=True)
    social_media_title = Column(String(500), unique=True, index=True, nullable=False)
    social_media_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    social_media_country_name = Column(String(50), nullable=False)
    social_media_description = Column(String(500), nullable=False)
    social_media_url = Column(String(500), nullable=False)
    social_media_status = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(engine)
