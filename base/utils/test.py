import pymysql

try:
    conn = pymysql.connect(
        host="localhost",
        user="demo",
        password="cK649m%%Q",
        database="myforeignjob_dbs",
        port=3306,
    )
    print("Connection successful", conn.get_server_info())
    conn.close()
except Exception as e:
    print("Error:", e)

from urllib.parse import quote_plus

password = quote_plus("your_password_here")
url = (f"mysql+pymysql://demo:"
       f"cK649m%%Q@mysql:3306/myforeignjob_dbs?charset=utf8")
print(f"URL = {url}")
