from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

# model

database = Database()
engine = database.get_db_connection()


class RuleVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "rules_table"

    rule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_country_id = Column(
        Integer,
        ForeignKey("country_table.country_id", onupdate="CASCADE",
                   ondelete="RESTRICT"),
        nullable=False,
    )
    rule_country_name = Column(String(500), nullable=False)
    rule_title = Column(String(255), nullable=False)
    rule_description = Column(String(255), nullable=False)


Base.metadata.create_all(engine)
