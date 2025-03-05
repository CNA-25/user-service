from fastapi import APIRouter, HTTPException  
from passlib.context import CryptContext
from prisma import Prisma
from pydantic import BaseModel
from utils import create_jwt

# Our hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# A function that verifys the given password against the hashed password from the database using the hashing context above
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

db = Prisma()

# Creating a basemodel for how the login credentials should look like
class UserLogin(BaseModel):
    email: str
    password: str

router = APIRouter()

# Our /login endpoint
@router.post("/login")
async def login(user: UserLogin):
    await db.connect()
    try:
        found_user = await db.user.find_unique(where={"email": user.email}) # checks if user exists

        if not found_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, found_user.password): # checks given password to database password
           raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_jwt(found_user) # creating the jwt for found user, called from middleware.py

        return {"access_token": token, "token_type": "bearer"} # returns the jwt
    finally:
        await db.disconnect()