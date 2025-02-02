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
    # identifier for the event - corresponds to objectid if stored in db
    identifier = None

    # datetime object or string
    date = None

    # deprecated
    start_time = None

    # string
    location = None

    # spec.EventTypes
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

    def __init__(self, dbobj=None):
        # import from DB -- assumes same format as to_db
        if dbobj:
            self.__from_db(dbobj)
        # otherwise empty

    def to_json(self):
        return json.dumps({"_id": self.identifier, "date": str(self.date), "start_time": self.start_time, "location":self.location, "event_type" : self.event_type.name, "event_name": self.event_name,"organizers":self.organizers,"post_author":self.post_author, "post_URL":self.post_URL, "fulltext":self.fulltext, "mediaurls":self.mediaurls})

    # from JSON to object, no validation
    def from_json(self, jsonblob):
        myjson = json.parse(jsonblob)
        self.identifier = jsonblob._id
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

    # dump the object to json - right now just a flat list
    def __from_db(self, dbobj):
        self.identifier = dbobj.get("_id", None)
        self.date = dbobj.get("date", None)
        self.start_time = dbobj.get("start_time", None)
        self.location = dbobj.get("location", None)
        event_type_name = dbobj.get("event_type", None)
        if event_type_name in EventTypes.__members__:
            self.event_type = EventTypes.__members__[event_type_name]
        else: 
            self.event_type = EventTypes.UNKNOWN
        self.event_name = dbobj.get("event_name", None)
        self.organizers = dbobj.get("organizers", [])
        self.post_author = dbobj.get("post_author", None)
        self.post_URL = dbobj.get("post_URL", None)
        self.fulltext = dbobj.get("fulltext", None)
        self.mediaurls = dbobj.get("mediaurls", [])

    # dump the object to json - right now just a flat list
    def to_db(self):
        return {"_id": self.identifier, "date": self.date, "start_time": self.start_time, "location":self.location, "event_type" : self.event_type.name, "event_name": self.event_name,"organizers":self.organizers,"post_author":self.post_author, "post_URL":self.post_URL, "fulltext":self.fulltext, "mediaurls":self.mediaurls}

    def __str__(self):
        return self.to_json()

    # returns a dict that defines the event as unique
    # WARNING needs to be kept identical to __key!
    # TODO right now this defines it using post URL as a factor
    # this is not sustainable, but I'm not sure how else to do it
    def get_search_pattern(self):
        return {"date": self.date, "location":self.location, "event_type" : self.event_type.name, "post_author":self.post_author, "post_URL":self.post_URL}

    # note: events with known IDs (self.identifier is set) are
    # defined as different from events that do not have a known ID
    # where relevant, use get_search_pattern to fetch the event from
    # the db and set the ID
    # yes this is horrible and messy
    def __key(self):
        if self.identifier:
            return self.identifier
        else:
            return (self.date, self.location, self.event_type.name, self.post_author, self.post_URL)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.__key() == other.__key()
        return NotImplemented
