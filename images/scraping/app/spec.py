import json

from enum import Enum
class EventTypes(Enum):
    UNKNOWN = 0
    RALLY = 1
    DEMONSTRATION = 2
    CULTURE = 3
    TALK = 4
    DISCUSSION = 5
    WORKSHOP = 6
    PLENARY = 7

    # guesses the event type based on heuristics
    # assumes wellformed argument, defaults to UNKNOWN
    def guess_event_type(text):
        return EventTypes.UNKNOWN


# the only purpose of this is to fix the json spec and handle it consistently
# there are probably better ways to do this but this felt quickest
class Event:

    # datetime object or string
    date = None

    # deprecated
    start_time = None

    # string
    location = None

    # spec.EventType
    event_type = None

    # string
    event_name = None

    # list[string]
    organizers = []

    # string
    post_author = None

    # URL as string
    post_URL = None

    # string
    fulltext = None

    # list[URL as string]
    mediaurls = []

    # empty constructor
    def __init__(self):
        pass

    # dump the object to json - right now just a flat list
    def to_json(self):
        return json.dumps({"date": str(self.date), "start_time": self.start_time, "location":self.location, "event_type" : self.event_type.name, "event_name": self.event_name,"organizers":self.organizers,"post_author":self.post_author, "post_URL":self.post_URL, "fulltext":self.fulltext, "mediaurls":self.mediaurls})

    # from JSON to object, no validation
    def from_json(self, jsonblob):
        myjson = json.parse(jsonblob)
        self.date = myjson.date
        self.start_time = myjson.start_time
        self.location = myjson.location
        self.event_type = myjson.event_type
        self.event_name = myjson.event_name
        self.organizers = myjson.organizers
        self.post_author = myjson.post_author
        self.post_URL = myjson.post_URL
        self.fulltext = myjson.fulltext
        self.mediaurls = myjson.mediaurls

    def __str__(self):
        return self.to_json()
