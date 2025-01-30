import instaloader
import json
import pickle

L = instaloader.Instaloader()

# scrape to json
def do_scrape(shortcode):
    if not shortcode:
        return None
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    return post

def cache_or_download(shortcode):
    # check cache
    # TODO pickle is unsafe but cheap - this code assumes the cache is a secure volume!
        # TODO add force-reload
    contents = None
    fp = None
    try:
        fp = open("/cache/" + shortcode, "rb")
        # open success -> read cache file
        # TODO avoid DoS due to huge files
        contents = pickle.load(fp)
        fp.close()
    #if file does not exist or throws EOF error, overwrite:
    except (FileNotFoundError, EOFError):
        try:
            fp = open("/cache/" + shortcode, "wb")
            # return instaloader post object - use for testing only!
            contents = do_scrape(shortcode)
            pickle.dump(contents, fp)
            fp.close()
        except OSError as e:
            print("Error while creating cache file", e)
    except OSError as e:
        print("Cache file exists but cannot be read, ", e)
    return contents
