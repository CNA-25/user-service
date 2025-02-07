import jwt
import passlib
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')

def authorise(request: Request):
    try:
        header = request.headers.get('Authorization') or None
        if header is None or not header.startswith("Bearer "): raise HTTPException(status_code=401)

        token = header.split(' ')[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, error="Expired signature")
        
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    except HTTPException:
        raise HTTPException(status_code=401, detail="HTTP Exception")
