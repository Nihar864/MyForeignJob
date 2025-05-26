from passlib.exc import InvalidHashError
from passlib.hash import argon2


def hash_password(password: str) -> str:
    """
    Request:
        password (str): The plaintext password to be hashed.

    Response:
        str: The securely hashed password string using Argon2 algorithm.

    Purpose:
        To securely hash a plaintext password for safe storage and later verification,
        utilizing the Argon2 hashing algorithm.

    Company Name: Softvan Pvt Ltd
    """
    return argon2.hash(password)


def verify_password(hashed_password: str, input_password: str) -> bool:
    """
    Request:
        hashed_password (str): The previously hashed password string.
        input_password (str): The plaintext password to verify against the hash.

    Response:
        bool: True if the input_password matches the hashed_password, False otherwise.

    Purpose:
        To verify if a given plaintext password matches the stored hashed password,
        handling invalid hash formats gracefully.

    Company Name: Softvan Pvt Ltd
    """
    print("verify")
    try:
        print(
            f"hashed_password: {hashed_password} & input_password: {input_password}")
        print("---->>>>>>>>>", argon2.verify(hashed_password, input_password))
        return argon2.verify(hashed_password, input_password)
    except InvalidHashError as e:
        raise ValueError(f"Invalid hash format: {e}")
