from sqlalchemy.orm import declarative_base

from base.db.database import Database, Base
from base.vo.country_vo import CountryVO


# Initialize database connection
Base = declarative_base()
database = Database()
engine = database.get_db_connection()
Base.metadata.create_all(engine)


print("Database tables created successfully.")
