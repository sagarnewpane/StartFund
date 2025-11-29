import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client["Cluster0"]  # your database name
users_collection = db["users"]
startups_collection = db["startup_pitch"]
