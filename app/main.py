from fastapi import FastAPI, Depends, Request, Response, status
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

app = FastAPI()

# Använd cors
# cors(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://store-frontend-git-cna-25-store-frontend.2.rahtiapp.fi/webshop/pages/login.html", "https://store-frontend-git-cna-25-store-frontend.2.rahtiapp.fi"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], 
    allow_headers=["Authorization", "Content-Type"], 
)

class User(BaseModel):
    id: int | None = None
    name: str
    email: str 
    password: str 
    phone: str
    dob: str
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

    return {"user_data":user}

#create a new user (register)
@app.post("/users")
async def create_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    created = await db.user.create(
        {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "phone": user.phone,
            "dob": user.dob
        }
    )
    return {"New user created": created}
    
#update user
@app.patch("/users/{id}")
async def update_user(id: int, user: User, decoded_jwt: dict = Depends(authorise)):
    hashed_password = pwd_context.hash(user.password)
    user = await db.user.update(
        where = {
            "id": id
        },
        data={
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "phone": user.phone,
            "dob": user.dob
        }
    )
    
    return {"message": "User updated"}

#delete user
@app.delete("/users/{id}")
async def delete_user(id: int, decoded_jwt: dict = Depends(authorise)):
    user = await db.user.delete(
    where={
        'id': id
        } 
    )
    return {"message": "User deleted"} 
