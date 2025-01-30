from fastapi import FastAPI
from contextlib import asynccontextmanager
from middleware import auth
from prisma import Prisma

app = FastAPI()

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