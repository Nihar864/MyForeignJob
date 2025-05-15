from sqlalchemy import Column, Integer, String, Boolean
from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class CountryVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "country_table"

    countryId = Column(Integer, primary_key=True, index=True)
    countryName = Column(String(500), unique=True, index=True, nullable=False)
    countryDescription = Column(String(500))
    countryImageNames = Column(String(500), nullable=False)
    countryImagePaths = Column(String(500), nullable=False)
    countryFlagImageName = Column(String(500), nullable=False)
    countryFlagImagePath = Column(String(500), nullable=False)
    countryCurrency = Column(String(50), nullable=False)
    showOnHomepageStatus = Column(Boolean, nullable=False, default=False)
    countryStatus = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(engine)
