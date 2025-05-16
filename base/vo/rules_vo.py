from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class Rule(Base, StatusMixin, TimestampMixin):
    __tablename__ = "rules"

    rule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_type = Column(String(100), nullable=False)
    country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", onupdate="CASCADE",
                   ondelete="RESTRICT"),
        nullable=False,
    )
    ruleTitle = Column(String(255), nullable=False)
    ruleDescription = Column(Text)
    effectiveDate = Column(Date, nullable=False)
    rulePublishStatus = Column(Boolean, default=False, nullable=False)

    country = relationship("Country", back_populates="rules")
    # only if Country model has `rules = relationship("Rule", back_populates="country")`


# Base.metadata.create_all(engine)
