from fastapi import FastAPI
from contextlib import asynccontextmanager
from middleware import auth
from prisma import Prisma
from pydantic import BaseModel

app = FastAPI()

fake_users_db = [{"name": "Anna"}, {"name": "Lisa"}, 
            {
                'name': 'caspian',
                'email': 'katt@example.com',
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

class User(BaseModel):
    name: str
    email: str 
    #password
    phone: str
    dob: str
    purchases: int
    adress: str
    data: str 

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

@app.get("/")
def read_root():
    return { "Hello": "user-service", "v": "0.1" }

@app.get("/users")
async def get_users():
    users = await db.user.find_many()
    return users

#get all users with hardcoded placeholder data
''' @app.get("/users")
async def get_users():
    return {"Users": fake_users_db} '''

#create a new user (register)
@app.post("/users")
def create_user(user: User):
    return user
