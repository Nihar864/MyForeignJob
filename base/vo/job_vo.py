from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class JobVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "job_table"

    jobId = Column(Integer, primary_key=True, index=True)
    jobTitle = Column(String(500), unique=True, index=True, nullable=False)
    jobCountryId = Column(
        Integer,
        ForeignKey("country_table.countryId", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    jobDescription = Column(String(500), nullable=False)
    jobLocation = Column(String(500), nullable=False)
    jobSalary = Column(Integer, nullable=False)
    jobStatus = Column(Boolean, nullable=False, default=False)


country = relationship("Country", back_populates="jobs")
Base.metadata.create_all(engine)
