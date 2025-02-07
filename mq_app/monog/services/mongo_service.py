import os, json, logging
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from mq_app.constants import RabbitMQConstants

if not load_dotenv(find_dotenv()):
    load_dotenv(os.path.join(os.getcwd(), '.env'))
else:
    load_dotenv(find_dotenv())

class MongoDBService:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB_NAME")
        if not db_name:
            logging.warning(f"Database name is None. Using 'cost_data_dump'.")
            db_name = RabbitMQConstants.MONGO_DB_NAME
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    # This method is used to insert data to the mongodb
    def insert_data(self, collection_name, data):
        if not collection_name:
            logging.warning(f"Collection name is None. Using 'cost_data_dump'.")
            collection_name = RabbitMQConstants.MONGO_COLLECTION_NAME

        collection = self.db[collection_name]
        collection.insert_one(data) #json.loads(data)
        logging.info(f'[+] Data inserted into {collection_name}: {data}')