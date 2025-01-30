from flask import Flask,redirect,url_for
import json
import scrape
import interpret
import output
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

    options = interpret.interpret_event_insta(post)
    if options:
        return [output.to_mastodon(i) for i in options] # let requester decide which is correct
    else:
        return "501 interpretation error"

@app.route('/')
def hello():
	return redirect(url_for('static', filename="main.html"))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
