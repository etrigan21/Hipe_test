from dotenv import dotenv_values
import os

configPath = os.path.abspath("config.env")
config = dotenv_values(configPath)

class AppConfig:
    host="localhost" #needs to be localhost for flutter 10.0.2.2 endpoint to work
    port=8080
    mongodbUri=config["MONGO_URL"]
    databaseName=config["DBNAME"]
    eventCollection=config["DBCOLLECTION"]
    startHour = 8
    endHour = 20