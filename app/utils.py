import jwt
import os
from dotenv import load_dotenv
import time, datetime
from datetime import timezone
from prisma.models import User

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')

def create_jwt(user_data: User):
    exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=TOKEN_EXPIRY)
    payload = {
        "sub": user_data.id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "exp": exp
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token
