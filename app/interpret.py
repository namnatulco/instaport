import instaloader
from dateparser.search import search_dates
import spec


# this method implements various methods to search for place names
# returns a list of strings
def search_place(text):
    return []

# this method implements various methods to search for organizers
# returns a list of strings
def search_organizers(text):
    return []

# guess event title
def guess_event_title(text):
    if not text:
        return ""
    return text.split("\n")[0]

# interprets the instaloader post object, assumes wellformed input
# returns a list of possible spec.Event objects
def interpret_event_insta(post):
    
    text = str(post.caption)

    # identify dates in the caption - will include time
    possible_dates = search_dates(text, languages=['de','en'])

    possible_locations = []
    if post.location:
        possible_locations.append(str(post.location))
    possible_locations.extend(search_place(text))

    if len(possible_locations) == 0:
        possible_locations = ["Ort unbekannt"]

    event_type = spec.EventTypes.guess_event_type(text)

    event_name = ""
    if post.title:
        event_name = str(post.title)
    else:
        event_name = guess_event_title(text)

    organizers = search_organizers(text)
    post_author = str(post.owner_username)
    if post_author:
        organizers.append(post_author) # assume author is organizer
    
    image = post.url

    post_URL = "https://www.instagram.com/p/" + str(post.shortcode) + "/"

    possible_events = []
    for eventdate in possible_dates:
        for loc in possible_locations:
            ev = spec.Event()
            ev.date = eventdate[1] # datetime object only
            ev.location = loc
            ev.event_type = event_type
            ev.event_name = event_name
            ev.organizers = organizers
            ev.post_author = post_author
            ev.post_URL = post_URL
            ev.fulltext = text
            ev.mediaurls = [image]
            possible_events.append(ev)

    return possible_events
