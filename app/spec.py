import json

# the only purpose of this is to fix the json spec and handle it consistently
# there are probably better ways to do this but this felt quickest
class Event:

    date = None
    start_time = None
    location = None
    event_type = None
    event_name = None
    organizers = []
    post_author = None
    post_URL = None

    # empty constructor
    def __init__(self):
        pass

    # empty constructor
    def __init__(self, jsonblob):
        self.from_json(jsonblob)

    # dump the object to json - right now just a flat list
    def to_json(self):
        return json.dumps({"date": self.date, "start_time": self.start_time, "location":self.location, "event_type" : self.event_type, "event_name": self.event_name,"organizers":self.organizers,"post_author":self.post_author, "post_URL":self.post_URL})

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
