from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

# Create the client
client = AsyncIOMotorClient(MONGO_URL)

# Connect to the database
db = client.console_app  # "console_app" is the database name

# Access the "user" collection
user_collection = db.user
revoked_tokens = db.revoked_tokens 