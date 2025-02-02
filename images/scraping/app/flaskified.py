from flask import Flask,redirect,url_for,request,render_template
import urllib
import json
import spec
import scrape
import interpret
import output
import re
import pymongo
from bson import ObjectId
mongo_db_connector = pymongo.MongoClient("mongodb://instaport_db_1:27017/") # TODO dont hardcode this

app = Flask(__name__, static_folder="static", template_folder="templates")

def get_by_shortcode(shortcode):
    post = None
    try:
        post = scrape.cache_or_download(shortcode[0])
    except Exception as e:
        print("parsing error", e)
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
        print("interpretation error")
        return None

@app.route('/set-choice-insta/', methods=['POST']) 
def set_by_objectid():

    objectid = request.form.get("objectid", default = None, type = str)
    feedback = request.form.get("feedback", default = None, type = str)

    # valiate objectid
    if not objectid or not type(objectid)==str:
        print("invalid objectid",objectid)
        return "fail"
    if not re.fullmatch(r'[a-z0-9]{24}', objectid.lower()):
        print("invalid objectid",objectid)
        return "fail"

    collection = mongo_db_connector["instaport"]["event-options-db"]
    if feedback:
        updatedict = {"$set": {"selected":True, "feedback":feedback}}
    else:
        updatedict = {"$set": {"selected":True}}
    print("updating in db" + objectid)
    oldobj = collection.find_one_and_update(
            {"_id": ObjectId(objectid)},
            updatedict
            )
    if not oldobj:
        return "error, " + objectid + " not a valid object"

    if "selected" in oldobj:
        return "was already selected"
    
    ev = spec.Event(dbobj=oldobj)
    if not ev:
        return "sorry, invalid object, this means the item in the database is broken"
    #return render_template('mastodon_publish.html', text=output.to_mastodon(ev))
    return redirect("https://mastodon.social/share?text=" + urllib.parse.quote_plus(output.to_mastodon(ev)))

@app.route('/select-insta/')
def select_by_shortcode():
    # TODO security checks

    # URL validator (https.+/p/)([a-zA-Z0-9-]{11})(/.*)?  \2
    targeturl = request.args.get("url-input", default = None, type = str)
    if not targeturl:
        return "400 missing or invalid argument"
    shortcode = scrape.extract_shortcode_insta_url(targeturl)
    if not shortcode:
        return "404 invalid shortcode"

    data = get_by_shortcode(shortcode)
    if not data:
        return "501 internal server error"

    options = [{"identifier":ev.identifier, "text":output.to_mastodon(ev)} for ev in data]
    return render_template('select-insta.html', options = options)

@app.route('/fetch/<shortcode_unchecked>')
def respond_fetch(shortcode_unchecked):
    # TODO security checks

    # URL validator (https.+/p/)([a-zA-Z0-9-]{11})(/.*)?  \2
    shortcode = scrape.extract_shortcode(shortcode_unchecked)
    if not shortcode:
        return "404 code not found"
    data = get_by_shortcode(shortcode)
    if not data:
        return "501 internal server error"
    return ["Option " + ev.identifier + " " + output.to_mastodon(ev) for ev in data]

@app.route('/main2')
def hello2():
	return redirect(url_for('static', filename="main2.html"))

@app.route('/')
def hello():
	return redirect(url_for('static', filename="main.html"))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
