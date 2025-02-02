# web server imports
from flask import Flask,redirect,url_for,request,render_template
from werkzeug.exceptions import BadRequest

app = Flask(__name__, static_folder="static", template_folder="templates")

# standard lib imports
import urllib
import json
import re
import logging

# database imports
import pymongo
from bson import ObjectId
mongo_db_connector = pymongo.MongoClient("mongodb://instaport_db_1:27017/") # TODO dont hardcode this

# app imports
import spec
import scrape
import interpret
import output
import instaport

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html', error_message=e), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_message=e), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', error_message=e), 500

'''
accept and store that the given object is a "correct" representation and forward the user to mastodon for posting

** Warning ** this will be deprecated soon
'''
@app.route('/set-choice-insta/', methods=['POST']) 
def set_by_objectid():
    objectid = request.form.get("objectid", default = None, type = str)
    feedback = request.form.get("feedback", default = None, type = str)

    # valiate objectid
    if not objectid or not type(objectid)==str:
        logging.warn("invalid objectid",objectid)
        raise BadRequest("Invalid ObjectId")

    if not re.fullmatch(r'[a-z0-9]{24}', objectid.lower()):
        logging.warn("malformed objectid",objectid)
        raise BadRequest("Invalid ObjectId")

    oldobj = instaport.update_event_by_objectid(objectid, feedback)
    if not oldobj:
        raise BadRequest("Invalid ObjectId")
    ev = spec.Event(dbobj=oldobj)
    if not ev:
        raise BadRequest("Could not convert document to Event")
    text = output.to_mastodon(ev)

    # redirect to mastodon URL
    return redirect("https://mastodon.social/share?text=" + urllib.parse.quote_plus(text))

'''
This page expects to be given a url through GET.
The shortcode is used as a unique identifier.
If provided, it retrieves data from the database (possibly scraping beforehand if needed) and returns a list of interpretations.
This is rendered in templates/select-insta.html. There, unauthenticated user can select their favorite interpretation and trigger a POST to store this along with notes.
'''
@app.route('/select-insta/')
def instagram_select_event_format():
    targeturl = request.args.get("url-input", default = None, type = str)
    if not targeturl:
        logging.warning("invalid url " + targeturl)
        raise BadRequest("Invalid URL")

    shortcode = scrape.extract_shortcode_insta_url(targeturl)
    if not shortcode:
        logging.warning("invalid shortcode " + shortcode)
        raise BadRequest("Could not parse shortcode from URL")

    data = instaport.instagram_event_by_shortcode(shortcode, platform="Mastodon")
    if not data:
        logging.warning("no valid data parsable")
        raise BadRequest("Could not parse shortcode from URL")

    return render_template('select-insta.html', options = data)

'''
redirect to static HTML main page
'''
@app.route('/')
def hello():
	return redirect(url_for('static', filename="main.html"))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
