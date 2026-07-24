from passlib.context import CryptContext

# bcrypt is intentionally slow. This work factor makes brute-force attacks computationally expensive,
# unlike MD5 or SHA-256 which are designed to be fast and are therefore vulnerable to rainbow tables 
# and modern GPU brute-forcing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
