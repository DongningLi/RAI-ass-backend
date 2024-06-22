import pymongo
import pymongo.mongo_client

url = "mongodb://mongodb:27017"
client = pymongo.MongoClient(url)

db = client["raidb1"]