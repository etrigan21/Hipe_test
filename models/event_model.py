from config.flask_config import AppConfig
from bson import json_util, ObjectId
from datetime import datetime 
from bson import json_util
from flask import jsonify
import json
from services import event_helper

class EventsModel(object):
    def __init__(self, eventDate, eventStartTime, eventEndTime, eventDescription, createDate, userId):
        self.eventDate = datetime.fromisoformat(eventDate)
        self.eventDescription = eventDescription
        self.createDate = datetime.fromisoformat(createDate)
        self.eventStartTime = datetime.fromisoformat(eventStartTime)
        self.eventEndTime = datetime.fromisoformat(eventEndTime)
        self.userId = userId

    def insertEvent(self, database):
        collection = database[AppConfig.eventCollection]
        try: 
            overlap = event_helper.acquireConinsidingEvents(collection, self.eventStartTime, self.userId, self.eventEndTime)
            if (self.eventStartTime.hour < AppConfig.startHour or self.eventStartTime.hour >= AppConfig.endHour) and (self.eventEndTime.hour >= AppConfig.endHour and self.eventEndTime.minute > 0):
                return {
                    "status": "failed", 
                    "message": "Event cannot be earlier than 8 am and later than 8 pm"
                }
            elif overlap: 
                return {
                    "status": "failed", 
                    "message": "Event overlaps with existing events"
                }
            else: 
                result = collection.insert_one(self.__dict__)
                return {
                    "status": "success", 
                    "message": str(result.inserted_id)
                }
        except Exception as error: 
            return {
                "status": "failed", 
                "message": str(error)
            }
    
    def toJson(self):
        return {
            "eventDate": self.eventDate,
            "eventDescription": self.eventDescription, 
            "createDate": self.createDate,
            "eventStartTime": self.eventStartTime, 
            "eventEndTime": self.eventEndTime, 
            "userId": self.userId
        }

    @staticmethod
    def getEvent(database, filter):
        collection = database[AppConfig.eventCollection]
        try:
            result = collection.find(filter)
            jsonified_result = event_helper.getFormatter(result)   
            return {
                "status": "success", 
                "message": jsonified_result
            }
        except Exception as error: 
            return {
                "status": "failed", 
                "message": str(error)
            }
    @staticmethod
    def deleteEvent(database, id):
        collection = database[AppConfig.eventCollection]
        try: 
            result = collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count == 0: 
                return {
                    "status": "failed", 
                    "message": f"{id} does not exist"
                }
            else: 
                return {
                "status": "success",
                "message": f"{id} deleted"
            }
        except Exception as error: 
            return {
                "status": "failed", 
                "message": str(error)
            }
    @staticmethod
    def updateEvent(database, id, event):
        try: 
            collection = database[AppConfig.eventCollection]
            result = collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
                "eventDescription": event["eventDescription"], 
                "eventStartTime": datetime.fromisoformat(event["eventStartTime"]), 
                "eventEndTime": datetime.fromisoformat(event["eventEndTime"])
            }})
            return {
                "status": "success", 
                "message": "Update Complete!"
            }
        except Exception as error: 
            return {
                "status": "failed", 
                "message": str(error)
            }