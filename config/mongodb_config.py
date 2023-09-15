from pymongo import MongoClient
from config.flask_config import AppConfig
class MongoConnector:
    eventClient = MongoClient(AppConfig.mongodbUri)
    eventDatabase = eventClient[AppConfig.databaseName]