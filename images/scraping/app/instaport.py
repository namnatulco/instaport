import spec
import scrape
import interpret
import output
import logging

import pymongo
from bson import ObjectId
mongo_db_connector = pymongo.MongoClient("mongodb://instaport_db_1:27017/") # TODO dont hardcode this

'''
Retrieve from Instagram based on shortcode. This is the code that identifies the post in Instagram.

Arguments:
    - shortcode (str): the shortcode to search for. This function assumes a valid and correct code.
'''
def instagram_get_by_shortcode(shortcode):
    post = None
    try:
        post = scrape.cache_or_download(shortcode)
    except Exception as e:
        logging.warning("failed while retrieving from instagram by shortcode",e)
        return None
    options = interpret.interpret_event_insta(post)
    if options:
        for ev in options:
            event_db_object = ev.to_db()
            if not event_db_object["_id"]:
                del event_db_object["_id"]
            
            # TODO optimize this by making it into a single query
            in_db = mongo_db_connector["instaport"]["event-options-db"].find_one(ev.get_search_pattern())
            if not in_db:
                event_db_object["_id"] = str(mongo_db_connector["instaport"]["event-options-db"].insert_one(event_db_object).inserted_id)
            else:
                event_db_object["_id"] = str(in_db["_id"])

            ev.identifier = event_db_object["_id"]

        results = set(options) # use set to remove duplicates
        return results
    else:
        logging.warning("failed while interpreting instagram post",post)
        return None

'''
Convert the Instagram post containing an event identified by shortcode into a series of possible mastodon posts
'''
def instagram_event_by_shortcode(shortcode, platform="Mastodon"):
    if platform != "Mastodon":
        logging.error("attempted to generate a post for a platform that is not yet implemented")
        return None

    data = instagram_get_by_shortcode(shortcode)
    if not data:
        return None
    else:
        return [{"identifier":ev.identifier, "text":output.to_mastodon(ev)} for ev in data]



'''
Update the database object associated with the passed objectid to indicate that the objectid is a valid representation and optionally feedback.

This method assumes well-formed and sanitized input. It will return the old database object per mongodb convention, or None if no object was found.
'''
def update_event_by_objectid(objectid, feedback=None):
    collection = mongo_db_connector["instaport"]["event-options-db"]

    # construct the update dict based on whether feedback was passed
    if feedback:
        updatedict = {"$set": {"selected":True, "feedback":feedback}}
    else:
        updatedict = {"$set": {"selected":True}}

    logging.info("updating in db", objectid)

    updated = collection.find_one_and_update(
            {"_id": ObjectId(objectid)},
            updatedict
            )
    return updated
