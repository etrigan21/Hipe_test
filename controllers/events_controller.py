from models.event_model import EventsModel
from config.mongodb_config import MongoConnector
from services import event_helper as EventHelper
import json 
def insertEvent(requestBody):
    eventDate = requestBody["eventDate"]
    eventStartTime = requestBody["eventStartTime"]
    eventEndTime = requestBody["eventEndTime"]
    eventDescription= requestBody["eventDescription"]
    createDate = requestBody["createDate"]
    userId = requestBody["userId"]
    event = EventsModel(eventDate, eventStartTime, eventEndTime, eventDescription, createDate, userId)
    return event.insertEvent(MongoConnector.eventDatabase)

def getEvent(filter):
    try: 
        query = EventHelper.getQueryBuilder(filter)
        return EventsModel.getEvent(MongoConnector.eventDatabase, query)
    except Exception as error: 
        return {
            "status": "failed", 
            "message": str(error)
        }

def deleteEvent(id):
    return EventsModel.deleteEvent( MongoConnector.eventDatabase, id)

def updateEvent(requestBody, id):
    return EventsModel.updateEvent(MongoConnector.eventDatabase, id, requestBody)