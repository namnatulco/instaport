from flask import Flask,redirect,url_for,request,render_template
import json
import scrape
import interpret
import output
import re
import pymongo
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


@app.route('/select-insta/')
def select_by_shortcode():
    # TODO security checks

    # URL validator (https.+/p/)([a-zA-Z0-9-]{11})(/.*)?  \2
    targeturl = request.args.get("url-input", default = None, type = str)
    if not targeturl:
        return "400 missing or invalid argument"
    shortcode_unchecked =  re.sub(r'(https.+/p/)([a-zA-Z0-9-]{11})(/.*)?', r"\2", targeturl)
    if not shortcode_unchecked:
        return "400 missing or invalid argument"
    shortcode = re.fullmatch(r'([a-zA-Z0-9-]{11})', shortcode_unchecked)
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
    shortcode = re.fullmatch(r'([a-zA-Z0-9-]{11})', shortcode_unchecked)
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
