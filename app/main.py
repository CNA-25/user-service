from fastapi import FastAPI, Depends, Request, Response, status
from contextlib import asynccontextmanager
from middleware import authorise
from prisma import Prisma
from pydantic import BaseModel
from passlib.context import CryptContext
from login import router as login_router
from utils import create_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

fake_users_db = [{"name": "Anna"}, {"name": "Lisa"}, 
            {
                'name': 'caspian',
                'email': 'katt@example.com',
                'password': 'password123',
                'phone': '1234567899',
                'dob': '1991-11-11T00:00:00Z',  
                'purchases': 5,
                'address': {
                    "street": "123 Main St",
                    "zipcode": "12345",
                    "city": "yayLand",
                    "country": "Country"
                },
                'data': {
                    "gender": "female",
                    "height": "180cm",
                    "weight": "100kg"
                }
            }]


""" class Adress(BaseModel):
    street: str
    zipcode: str
    city: str
    country: str

class Data(BaseModel):
    gender: str
    height: str
    weight: str
 """
class User(BaseModel):
    id: int | None = None
    name: str
    email: str 
    password: str
    phone: str
    dob: str
    purchases: int
    #adress: Adress
    #data: Data
    updatedAt: str

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

app.include_router(login_router)

@app.get("/")
def read_root():
    return { "Hello": "user-service", "v": "0.1" }


@app.get("/users")
async def get_users(request: Request, response: Response, decoded_jwt: dict = Depends(authorise)):
    print("got to /users")
    #users = await db.user.find_many()
    try:
        user = await db.user.find_unique(
            where={
                'id': int(decoded_jwt['sub']),
        })
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"error":"User not found"}

    return {"User_data":user}

#create a new user (register)
@app.post("/users")
async def create_user(user: User):
    #password = encryptPassword(user.password)
    hashed_password = pwd_context.hash(user.password)
    created = await db.user.create(
        {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "phone": user.phone,
            "dob": user.dob,
            "purchases": user.purchases,
            #"address": {user.adress},
            #"data": {user.data},
            "updatedAt": user.updatedAt
        }
    )
    return {"New user created": created}
    
#update user, send id in body
@app.patch("/users")
async def update_user(user: User, decoded_jwt: dict = Depends(authorise)):
    user = await db.user.update(
        where = {
            "id": user.id
        },
        data={
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "dob": user.dob,
            "purchases": user.purchases,
            #"address": {user.adress},
            #"data": {user.data},
            "updatedAt": user.updatedAt
        }
    )
    
    return {"message": "User updated"}

#delete user, endpoint according to id
@app.delete("/users/{id}")
async def delete_user(id: int, decoded_jwt: dict = Depends(authorise)):
    user = await db.user.delete(
    where={
        'id': id
        } 
    )
    return {"message": "User deleted"} 
