from dataclasses import dataclass
import os 
import pymongo

@dataclass
class EnviornmentVariable:
    '''
    Holds enviormnent variables for the database connection
    '''
    mongo_db_url: str = os.getenv('MONGO_DB_URL')

env_var      = EnviornmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)