from passlib.context import CryptContext

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return bcrypt.hash(password)


def verify_password(password: str, hashed_password: str):
    return bcrypt.verify(password, hashed_password)
