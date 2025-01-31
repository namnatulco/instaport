import instaloader
import json
import pymongo

L = instaloader.Instaloader()
c = pymongo.MongoClient("mongodb://instaport_db_1:27017/") # TODO dont hardcode this

# scrape to json
def do_scrape(shortcode):
    if not shortcode:
        return None
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    return post

def cache_or_download(shortcode, force_download=False):
    collection = c["instaport"]["insta-raw"]
    res = collection.find_one({"shortcode":shortcode})

    if not force_download and res:
        return res
    else:
        print("scraping")
        # proceed with scraping
        data = do_scrape(shortcode)

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

        # store obj in db 
        print("dbwrite", data_dict)
        collection.insert_one(data_dict)
        return data_dict
