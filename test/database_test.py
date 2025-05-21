from passlib.exc import InvalidHashError
from passlib.hash import argon2

# Plain text password
plain_password = "admin@123"

# Hash the password
hashed_password = argon2.hash(plain_password)

print("Hashed Password:", hashed_password)


def verify_password(hashed_password, input_password):
    print("varify")
    try:
        print(argon2.verify(input_password, hashed_password))
        return argon2.verify(input_password, hashed_password)
    except InvalidHashError as e:
        print(e)


verify_password(hashed_password, plain_password)
