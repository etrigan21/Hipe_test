from datetime import datetime
from bson.json_util import dumps, loads
def getQueryBuilder(args):
    if not "userId" in args: 
        raise Exception("Missing UserId")
    query = {"userId": int(args["userId"])}
    if "eventDate" in args: 
        query["eventDate"] = datetime.fromisoformat(args["eventDate"])
    if "eventStartFilter" in args: 
        query["eventStartTime"] = {"$gte": datetime.fromisoformat(args["eventStartFilter"])}
    if "eventEndFilter" in args: 
        query["eventStartTime"] = {"$lte": datetime.fromisoformat(args["eventEndFilter"])}
    if "eventEndFilter" in args and "eventStartFilter" in args: 
        query["eventStartTime"] = {"$lte": datetime.fromisoformat(args["eventEndFilter"]), "$gte": datetime.fromisoformat(args["eventStartFilter"])}
    return query

def getFormatter(events):
    final_events= []
    for event in events:
        event["_id"] = str(event["_id"])
        event["eventStartTime"] = event["eventStartTime"].isoformat(sep="T")
        event["eventEndTime"] = event["eventEndTime"].isoformat(sep="T")
        event["createDate"] = event["createDate"].isoformat(sep="T")
        event["eventDate"] = event["eventDate"].isoformat(sep="T")
        final_events.append(event)
    return loads(dumps((final_events)))

def checkForOverlap(startTime1, endTime1, startTime2, endTime2):
    if (startTime1 < startTime2 < endTime1) or (startTime1 < endTime2< endTime1) or (startTime2 < startTime1 < endTime2) or (startTime2 < endTime1 < endTime2):
        return True
    else: 
        return False

def acquireConinsidingEvents(collection, eventStartTime, userId, eventEndTime):
    copyStartTime = eventStartTime
    dayStart = copyStartTime.replace(hour=0, minute=0)
    dayEnd = copyStartTime.replace(hour=23, minute=59)
    existingEvents = list(collection.find({"userId": userId, "eventStartTime": {"$gte": dayStart, "$lte": dayEnd}}))
    for event in existingEvents: 
        event_2_start_time = event["eventStartTime"]
        event_2_end_time = event["eventEndTime"]
        overlap = checkForOverlap(eventStartTime, eventEndTime, event_2_start_time, event_2_end_time)
        if overlap == True: 
            return True
        else: 
            pass
    return False