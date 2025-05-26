from datetime import datetime

import mysql.connector
import pytz

from base.utils.constant import (
    constant,
    Constant,
)  # Update the import path as per your structure
from base.utils.password_hash import hash_password

hash_pwd = Constant.ADMIN_PASSWORD


def get_current_time():
    """
    Request:
        None

    Response:
        Returns the current date and time as a formatted string in 'YYYY-MM-DD HH:MM:SS' format
        based on the Asia/Kolkata timezone.

    Purpose:
        To provide a consistent timestamp for database operations adjusted to Indian Standard Time (IST).

    Company Name: Softvan Pvt Ltd
    """
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")


def get_connection_cursor():
    """
    Request:
        None

    Response:
        Returns a tuple containing a MySQL cursor object and the database connection object.

    Purpose:
        Establishes and provides a connection and cursor to the MySQL database
        for executing SQL queries.

    Company Name: Softvan Pvt Ltd
    """
    conn = mysql.connector.connect(
        host=constant.DB_HOST,
        port=constant.DB_PORT,
        user=constant.DB_USERNAME,
        password=constant.DB_PASSWORD,
        database=constant.DB_NAME,
    )
    return conn.cursor(), conn


def execute_query(query, values=None):
    """
    Request:
        query (str): SQL query string with placeholders for parameterized execution.
        values (tuple, optional): Tuple of values to safely replace placeholders in the query.

    Response:
        None (prints status messages indicating success or failure).

    Purpose:
        Executes a given SQL query with optional parameters,
        commits the transaction, and manages resource cleanup.

    Company Name: Softvan Pvt Ltd
    """
    cursor, conn = get_connection_cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
        print("✅ Inserted:", cursor.rowcount, "record(s)")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        cursor.close()
        conn.close()


def insert_single_role():
    """
    Request:
        None

    Response:
        None (prints insertion status).

    Purpose:
        Inserts a single administrative role record into the 'role_table' with
        a role name, deletion status, and timestamps.

    Company Name: Softvan Pvt Ltd
    """
    now = get_current_time()
    query = """
            INSERT INTO role_table (role_name, is_deleted, created_at,
                                    updated_at)
            VALUES (%s, %s, %s, %s) \
            """
    values = (constant.ROLE_ADMIN.upper(), 0, now, now)
    execute_query(query, values)


def insert_single_admin():
    """
    Request:
        None

    Response:
        None (prints insertion status).

    Purpose:
        Inserts a default administrator user into the 'admin_table' with
        hashed password, role linkage, deletion status, and timestamps.

    Company Name: Softvan Pvt Ltd
    """
    now = get_current_time()
    hashed_pwd = hash_password(constant.ADMIN_PASSWORD)

    query = """
            INSERT INTO admin_table (username, password, role, is_deleted,
                                     created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s) \
            """
    values = (
        constant.ADMIN_USERNAME,
        hashed_pwd,
        1,  # FK to role_table (assumes role ID is 1)
        0,
        now,
        now,
    )
    execute_query(query, values)


# --- Execute ---
insert_single_role()
insert_single_admin()
