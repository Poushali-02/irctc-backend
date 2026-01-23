from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT=MongoClient(os.getenv("MONGO_URI"))
DATABASE=CLIENT[os.getenv("MONGO_DB_NAME")]
