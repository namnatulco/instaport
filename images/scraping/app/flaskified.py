from flask import Flask,redirect,url_for
import json
import scrape
import re

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
    except:
        return "501 error fetching post"

    # return a mostly unfiltered json dump as temporary dump
    return json.dumps({"post-date":str(post.date), "post-author":str(post.owner_username), "post-title":str(post.title), "post-thumb":str(post.url), "caption":str(post.caption), "location":str(post.location)})

@app.route('/')
def hello():
	return redirect(url_for('static', filename="main.html"))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
