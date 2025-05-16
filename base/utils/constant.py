import os
from configparser import ConfigParser, NoSectionError

# Initialize config parser
configure = ConfigParser()

# ✅ Correct path: move up from 'base/utils' to 'MyForeignJob'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # /MyForeignJob/base/utils
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))  # /MyForeignJob
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.ini")  # /MyForeignJob/config.ini

# Check config file existence
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"The config file '{CONFIG_PATH}' does not exist.")

# Load the config file
configure.read(CONFIG_PATH)


# Now load the configuration values
class Constant:
    try:
        DB_SCHEME = configure.get("DB_CONFIG", "db_scheme")
        DB_USERNAME = configure.get("DB_CONFIG", "db_username")
        DB_PASSWORD = configure.get("DB_CONFIG", "db_password")
        DB_HOST = configure.get("DB_CONFIG", "db_host")
        DB_PORT = configure.get("DB_CONFIG", "db_port")
        DB_NAME = configure.get("DB_CONFIG", "db_name")

        DATABASE_URL = (
            f"{DB_SCHEME}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        ACCESS_TOKEN = configure.get("TOKEN_CONFIG", "ACCESS_TOKEN")
        REFRESH_TOKEN = configure.get("TOKEN_CONFIG", "REFRESH_TOKEN")
        ACCESS_TOKEN_EXP = int(configure.get("TOKEN_CONFIG", "ACCESS_TOKEN_EXP"))
        REFRESH_TOKEN_EXP = int(configure.get("TOKEN_CONFIG", "REFRESH_TOKEN_EXP"))
        TIME_OUT_MAX_AGE = int(configure.get("TOKEN_CONFIG", "TIME_OUT_MAX_AGE"))

        ENCODING = configure.get("SECURITY_CONFIG", "ENCODING")
        HASH_ALGORITHM = configure.get("SECURITY_CONFIG", "HASH_ALGORITHM")
        JWT_SECRET_KEY = configure.get("SECURITY_CONFIG", "JWT_SECRET_KEY")

        ROLE_ADMIN = configure.get("ROLE_CONFIG", "ROLE_ADMIN")
        ROLE_USER = configure.get("ROLE_CONFIG", "ROLE_USER")

        SECRET_KEY = configure.get("APP_SECRET", "SECRET_KEY")
        API_KEY = configure.get("APP_SECRET", "API_KEY")

        ADMIN_USERNAME = configure.get("ADMIN_CREDENTIALS", "ADMIN_USERNAME")
        ADMIN_PASSWORD = configure.get("ADMIN_CREDENTIALS", "ADMIN_PASSWORD")

    except NoSectionError as e:
        raise Exception(f"Missing section in config.ini: {str(e)}")


# You can now access your constants through the 'Constant' class
constant = Constant()
