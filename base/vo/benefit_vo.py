from sqlalchemy import Column, Integer, String, ForeignKey

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class BenefitVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "benefit_table"

    benefit_id = Column(Integer, primary_key=True, index=True)
    benefit_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    benefit_country_name = Column(String(50), nullable=False)
    benefit_title = Column(String(500), index=True, nullable=False)
    benefit_description = Column(String(500), nullable=False)
    # benefit_image_name = Column(String(500), nullable=False)
    # benefit_image_path = Column(String(500), nullable=False)


Base.metadata.create_all(engine)
