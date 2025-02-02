import instaloader
import json
import re
import pymongo
mongo_db_connector = pymongo.MongoClient("mongodb://instaport_db_1:27017/") # TODO dont hardcode this

L = instaloader.Instaloader()

'''
Validate Instagram shortcode format.

Argumets:
    shortcode - string representation of the shortcode to be checked

Returns:
    - a new instance of the shortcode, if the format is valid
    - None, otherweise
'''
def extract_shortcode(shortcode):
    res = re.fullmatch(r'([a-zA-Z0-9_-]{11})', shortcode)
    if res:
        return res[0]
    else:
        return None

'''
Helper function to consistently extract shortcodes from instagram URLs.
This function also validates the format of the shortcode using `extract_shortcode`.

Arguments:
    - url - str representation of the URL to be converted

Returns:
    - None, if no valid shortcode could be extracted
    - the shortcode as string
'''
def extract_shortcode_insta_url(url):
    res = re.sub(r'(https.+/p/)([a-zA-Z0-9_-]{11})(/.*)?', r"\2", url)
    if not res:
        return None
    sc = extract_shortcode(res)
    return sc

'''
Downlodas a given shortcode from instagram and scrapes together a dictionary representation of the data.

Arguments:
    - shortcode - str representation of the shortcode that identifies the instagram post to be downloaded

Returns:
    - None, if the parser returns None
    - data dictionary with relevant fields, on parsing success
'''
def instagram_download(shortcode):
    data = instaloader.Post.from_shortcode(L.context, shortcode)
    if not data:
        logging.error("instaloader returned None", shortcode)
        return None

    data_dict = {"shortcode":shortcode}

    # parse/flatten objects for storage as strings
    if data.accessibility_caption:
        data_dict["accessibility_caption"] = str(data.accessibility_caption)
    else:
        data_dict["accessibility_caption"] = None

    data_dict["caption"] = str(data.caption)

    if data.caption_hashtags:
        data_dict["caption_hashtags"] = [str(x) for x in data.caption_hashtags]

    if data.caption_mentions:
        data_dict["caption_mentions"] = [str(x) for x in data.caption_mentions]

    # data.comments not implemented

    if data.date:
        data_dict["date"] = data.date
        

    # date_utc and date_local not implemented
    # .getcomments not implemented
    # .get_is_videos not implemented
    # get_likes not implemented

    # I *thinK* this is a list of URLs to all of the media items
    # but idk why these do not have accessibility captions
    scn = data.get_sidecar_nodes()
    data_dict["media_slide_urls"] = [str(x.display_url) for x in scn]

    # is_pinned
    # is_sponsored
    # is_video
    # likes
    # location is always empty unless logged in
    # mediacount
    # mediaid
    # owner_id
    # owner_profile
    data_dict["owner_username"] = str(data.owner_username)

    # pcaption
    # profile
    # shortcode -> already included
    # sponsored_users
    data_dict["tagged_users"] = [str(x) for x in data.tagged_users]

    if data.title:
        data_dict["title"] = str(data.title)
    else:
        data_dict["title"] = None

    # typename

    data_dict["url"] = str(data.url)

    # video_duration
    # video_url
    if data.video_url:
        data_dict["video_url"] = str(data.video_url)
    else:
        data_dict["video_url"] = None

    # video_view_count
    # viewer_has_liked

    return data_dict
