import jwt
import os
from dotenv import load_dotenv
import datetime
from datetime import timezone
from prisma.models import User

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')

#create jwt token
def create_jwt(user_data: User):
    exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=int(TOKEN_EXPIRY))
    payload = {
        "sub": str(user_data.id),
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "exp": exp
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token
