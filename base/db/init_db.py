from sqlalchemy.orm import declarative_base

from base.db.database import Database

# Initialize database connection
Base = declarative_base()
database = Database()
engine = database.get_db_connection()
Base.metadata.create_all(engine)

print("Database tables created successfully.")
