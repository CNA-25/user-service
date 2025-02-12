import jwt
import os
from dotenv import load_dotenv
import time, datetime
from datetime import timezone

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')

def create_jwt(user_data):
    exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=TOKEN_EXPIRY)
    print(exp)
    print(type(user_data))
    """payload = {
        "sub": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "exp": exp
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token"""
