import spec
import os

# generates a text only mastodon post (max 500 chars)
# expects spec.Event
# assumes wellformed input
def to_mastodon(event, maxlen=500):
    result = "{date}, {location}: {event_name} - {post_author} ( {post_URL} )".format(
            date = str(event.date),
            location = event.location,
            event_name = event.event_name,
            post_author = event.post_author,
            post_URL = event.post_URL)
    if len(result) >= maxlen:
        # TODO consider that URLs are considered fixed length strings
        # use format that cuts off event name instead of url
        result = "{date}, {location} ({post_author} - {post_URL} ): {event_name}".format(
            date = str(event.date),
            location = event.location,
            event_name = event.event_name,
            post_author = event.post_author,
            post_URL = event.post_URL)
        result = result[0:maxlen-1]
    else:
        # there is space -- add the full text on a new line, then trim
        result += os.linesep
        result += event.fulltext
        result = result[0:maxlen-1]

    return result
