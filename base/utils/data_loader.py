import os
from datetime import datetime
import mysql.connector
from base.utils.constant import constant, \
    Constant  # Update the import path as per your structure
from base.utils.password_hash import hash_password
import pytz

hash_pwd = Constant.ADMIN_PASSWORD

def get_current_time():
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

def get_connection_cursor():
    conn = mysql.connector.connect(
        host=constant.DB_HOST,
        port=constant.DB_PORT,
        user=constant.DB_USERNAME,
        password=constant.DB_PASSWORD,
        database=constant.DB_NAME,
    )
    return conn.cursor(), conn

def execute_query(query, values=None):
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


# --- Data Inserts ---
def insert_single_role():
    now = get_current_time()
    query = """
        INSERT INTO role_table (role_name, is_deleted, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
    """
    values = (constant.ROLE_ADMIN.upper(), 0, now, now)
    execute_query(query, values)


def insert_single_admin():
    now = get_current_time()
    hashed_pwd = hash_password(constant.ADMIN_PASSWORD)

    query = """
        INSERT INTO admin_table (username, password, role, is_deleted, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        constant.ADMIN_USERNAME,
        hashed_pwd,
        1,  # FK to role_table (assumes role ID is 1)
        0,
        now,
        now
    )
    execute_query(query, values)


# --- Execute ---
insert_single_role()
insert_single_admin()
