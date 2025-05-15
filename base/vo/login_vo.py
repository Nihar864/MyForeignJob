from sqlalchemy import Column, Integer, String, Boolean

from base.db.database import Base, Database
from base.mixins import StatusMixin, TimestampMixin

database = Database()
engine = database.get_db_connection()


class LoginVO(Base, StatusMixin, TimestampMixin):
    __tablename__ = "login_table"

    login_id = Column(Integer, primary_key=True, index=True)
    login_username = Column(String(50), unique=True, index=True,
                            nullable=False)
    login_password = Column(String(128), nullable=False)
    login_status = Column(Boolean, nullable=False, default=False)


# Base.metadata.create_all(engine)

# INSERT INTO login_table (loginUsername, loginPassword, loginStatus, createdAt, updatedAt, isDeleted)
# VALUES ('new_user', 'secure_password123', TRUE, NOW(), NOW(), FALSE);
