## connect to database
import asyncio
from prisma import Prisma
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

async def main() -> None:
    db = Prisma()
    await db.connect()

    print("Connected to the database!")

    await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
