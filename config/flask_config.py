from dotenv import dotenv_values
import os

configPath = os.path.abspath("config.env")
config = dotenv_values(configPath)

class AppConfig:
    host="localhost" #Only localhost for testing
    port=8080
    mongodbUri=config["MONGO_URL"]
    databaseName=config["DBNAME"]
    eventCollection=config["DBCOLLECTION"]
    startHour = 8
    endHour = 20