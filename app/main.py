from fastapi import FastAPI, Depends, Request, Response, status, HTTPException
from contextlib import asynccontextmanager
from middleware import authorise, cors
from prisma import Prisma
from pydantic import BaseModel
from passlib.context import CryptContext
from login import router as login_router
from utils import create_jwt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Address(BaseModel):
    street: str
    zipcode: str
    city: str
    country: str

class Data(BaseModel):
    gender: str
    height: str
    weight: str
class User(BaseModel):
    id: int | None = None
    name: str
    email: str 
    password: str 
    phone: str
    dob: str
    address: Address = None
    data: Data = None
    updatedAt: str| None = None

db = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This allows the api to connect to prisma on startup and then disconnect on shutoff
    print("Connecting to the database...")
    await db.connect()
    yield  # Allows app to run, while keeping the DB connection open
    print("Disconnecting from the database...")
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

# Använd cors
cors(app)

app.include_router(login_router)

@app.get("/")
def read_root():
    return { "Hello": "user-service", "v": "0.1" }


@app.get("/users")
async def get_users(request: Request, response: Response, decoded_jwt: dict = Depends(authorise)):
    #users = await db.user.find_many()
    try:
        if(decoded_jwt['role'] == 'admin'):
            users = await db.user.find_many()
            return {"user_data":users}
        else:
            return{"error": "Unauthorised"}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"error":"User not found"}

@app.get("/users/{id}")
async def get_users(id: int, request: Request, response: Response, decoded_jwt: dict = Depends(authorise)):
    print("got to /users")
    #users = await db.user.find_many()
    try:
        if(decoded_jwt['role'] == 'admin'):
            user = await db.user.find_unique(
            where={
                'id': id,
        })
        else:
            user = await db.user.find_unique(
                where={
                    'id': int(decoded_jwt['sub']),
            })
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"error":"User not found"}

    return {"user_data":user}

#create a new user (register)
@app.post("/users")
async def create_user(user: User):
    try:
        hashed_password = pwd_context.hash(user.password)
        created = await db.user.create(
            data = {
                "name": user.name,
                "email": user.email,
                "password": hashed_password,
                "phone": user.phone,
                "dob": user.dob,
                "address": user.address or {},
                "data": user.data or {}
            }
        )
    except Exception as e:
        return {"Could not create user, error:": e}
    token = create_jwt(created)
    return {"message":"user created", "access_token": token, "token_type": "bearer"}
    #return {"New user created": created}
    
#update user
@app.patch("/users/{id}")
async def update_user(id: int, user: User, decoded_jwt: dict = Depends(authorise)):
    hashed_password = pwd_context.hash(user.password)
    #allow admin to update user with any id
    if(decoded_jwt['role'] == "admin"):
        user = await db.user.update(
            where = {
                "id": id
            },
            data={
                "name": user.name,
                "email": user.email,
                "password": hashed_password,
                "phone": user.phone,
                "dob": user.dob,
                "address": user.address or {},
                "data": user.data or {}
            }
        )
    #users can only update their own profile
    elif(id == int(decoded_jwt['sub'])):
        user = await db.user.update(
            where = {
                "id": int(decoded_jwt['sub'])
            },
            data={
                "name": user.name,
                "email": user.email,
                "password": hashed_password,
                "phone": user.phone,
                "dob": user.dob,
                "address": user.address or {},
                "data": user.data or {}
            }
        )
    else:
        raise HTTPException(status_code=403, detail="You are not allowed to update another users profile")
    
    return {"message": "User updated"}

#delete user
@app.delete("/users/{id}")
async def delete_user(id: int, decoded_jwt: dict = Depends(authorise)):
    #allow admin to delete user with any id
    if(decoded_jwt['role'] == "admin"):
        user = await db.user.delete(
        where={
            'id': id
            } 
        )
    #users can only delete their own profile
    elif (id == int(decoded_jwt['sub'])):
                user = await db.user.delete(
        where={
            'id': int(decoded_jwt['sub'])
            } 
        )
    else:
        raise HTTPException(status_code=403, detail="You are not allowed to delete another users profile")
    return {"message": "User deleted"}
