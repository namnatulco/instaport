import instaloader
import json

L = instaloader.Instaloader()

# scrape to json
def do_scrape(shortcode):
    if not shortcode:
        return None
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    return post
