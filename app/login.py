from fastapi import APIRouter, HTTPException, Request  
from passlib.context import CryptContext
import jwt
from prisma import Prisma
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from middleware import authorise
from utils import create_jwt

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

db = Prisma()

class UserLogin(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin):
    db = Prisma()

    await db.connect()
    try:
        found_user = await db.user.find_unique(where={"email": user.email})

        if not found_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, found_user.password):
           raise HTTPException(status_code=401, detail="Invalid credentials")

        token_data = {
            "sub": found_user.email,
            "name": found_user.name,
        }

        #token = jwt.encode(token_data, JWT_SECRET, algorithm=ALGORITHM)
        token = create_jwt(found_user)

        return {"access_token": token, "token_type": "bearer", "message": "Login endpoint is being worked on!"}
    finally:
        await db.disconnect()
