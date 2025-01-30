## connect to database
import asyncio, json
from prisma import Prisma
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

async def main() -> None:
    db = Prisma()

    try:
        # Connect to the database
        await db.connect()
        print("Connected to the database!")

        # Perform any database operations here (if needed)
        # Create a user
        user = await db.user.create(
             data={
                'name': 'Iris',
                'email': 'sliris@example.com',
                'phone': '123456789',
                'dob': '1991-11-11T00:00:00Z',  # Format is YYYY-MM-DDTHH:mm:ssZ
                'purchases': 5,
                # JSON objects
                'address': json.dumps({
                    "street": "123 Main St",
                    "zipcode": "12345",
                    "city": "yayLand",
                    "country": "Country"
                }),
                'data': json.dumps({
                    "gender": "female",
                    "height": "180cm",
                    "weight": "100kg"
                })
            }
        )

        print("User created:", user)

    except Exception as e:
        print(f"Error connecting to the database: {e}")

    finally:
        # Disconnect after operations are done
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

