import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


hashed_pwd = hash_password("admin@123")
print(hashed_pwd)
