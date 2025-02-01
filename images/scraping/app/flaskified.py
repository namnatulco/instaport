from flask import Flask,redirect,url_for
import json
import scrape
import interpret
import output
import re
import pymongo
mongo_db_connector = pymongo.MongoClient("mongodb://instaport_db_1:27017/") # TODO dont hardcode this

app = Flask(__name__, static_folder="static")

@app.route('/fetch/<shortcode_unchecked>')
def get_by_shortcode(shortcode_unchecked):
    # TODO security checks

    # URL validator (https.+/p/)([a-zA-Z0-9-]{11})(/.*)?  \2
    shortcode = re.fullmatch(r'([a-zA-Z0-9-]{11})', shortcode_unchecked)
    if not shortcode:
        return "404 code not found"
    post = None
    try:
        post = scrape.cache_or_download(shortcode[0])
    except Exception as e:
        print("parsing error", e)
        return "501 error fetching post"

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
        return ["Option " + ev.identifier + " " + output.to_mastodon(ev) for ev in results]
    else:
        print("interpretation error")
        return "501 interpretation error"

@app.route('/')
def hello():
	return redirect(url_for('static', filename="main.html"))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
