from sqlalchemy import Column, Integer, String, Boolean

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class CountryVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "country_table"

    country_id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(500), index=True, nullable=False)
    country_description = Column(String(500))
    country_image_names = Column(String(500), nullable=False)
    country_image_paths = Column(String(500), nullable=False)
    country_flag_image_name = Column(String(500), nullable=False)
    country_flag_image_path = Column(String(500), nullable=False)
    country_currency = Column(String(50), nullable=False)
    show_on_homepage_status = Column(Boolean, nullable=False, default=False)
    country_status = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(engine)
