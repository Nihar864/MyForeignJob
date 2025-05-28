from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class FaqVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "faq_table"

    faq_id = Column(Integer, primary_key=True, index=True)
    faq_title = Column(String(500), index=True, nullable=False)
    faq_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    faq_country_name = Column(String(50), nullable=False)
    faq_description = Column(String(500), nullable=False)


country = relationship("Country", back_populates="faq")
Base.metadata.create_all(engine)
