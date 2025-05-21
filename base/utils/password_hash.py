from passlib.exc import InvalidHashError
from passlib.hash import argon2


def hash_password(password):
    return argon2.hash(password)


def verify_password(hashed_password, input_password):
    print("varify")
    try:
        print(
            f"hashed_password: {hashed_password} & input_password: {input_password}")
        print("---->>>>>>>>>", argon2.verify(hashed_password, input_password))
        return argon2.verify(hashed_password, input_password)
    except InvalidHashError as e:
        raise ValueError(f"Invalid hash format: {e}")
