import instaloader
import json

L = instaloader.Instaloader()

# scrape to json
def do_scrape(shortcode):
    if not shortcode:
        return None
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    return post

def post_to_json(post)
    return json.dumps({"post-date":str(post.date), "post-author":str(post.owner_username), "post-title":str(post.title), "post-thumb":str(post.url), "caption":str(post.caption), "location":str(post.location)})
