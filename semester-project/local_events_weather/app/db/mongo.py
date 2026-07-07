import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

event_details_collection = db["event_details"]
weather_api_responses_collection = db["weather_api_responses"]
user_notes_collection = db["user_notes"]