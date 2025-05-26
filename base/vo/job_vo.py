from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class JobVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "job_table"

    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(500), unique=True, index=True, nullable=False)
    job_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    job_country_name = Column(String(500), nullable=False)
    job_description = Column(String(500), nullable=False)
    job_location = Column(String(500), nullable=False)
    job_salary = Column(Integer, nullable=False)
    job_status = Column(Boolean, nullable=False, default=False)

    # country = relationship("Country", back_populates="jobs")


Base.metadata.create_all(engine)
