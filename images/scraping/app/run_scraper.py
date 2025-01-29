from sys import argv

if len(argv) != 2 or not argv[1] or len(argv[1]) != 11:
    print("Error, provide exactly one shortcode as argument (shortcodes have a length of 11 chars)")
    if(argv[1]):
        print("provided first argument is:",argv[1])
    exit(1)

shortcode=argv[1]

# check cache
# TODO pickle is unsafe but cheap - this code assumes the cache is a secure volume!
# TODO add force-reload
import pickle
contents = None
fp = None
try:
    fp = open("/cache/" + shortcode, "rb", encoding="utf-8")
    # open success -> read cache file
    # TODO avoid DoS due to huge files
    contents = pickle.load(fp)
    fp.close()
except FileNotFoundError:
    try:
        fp = open("/cache/" + shortcode, "w", encoding="utf-8")
        import scrape
        # return instaloader post object - use for testing only!
        post = scrape.do_scrape(shortcode)
        pickle.dump(post, fp)
        fp.close()
    except OSError e:
        print("Error while creating cache file", e)
except OSError e:
    print("Cache file exists but cannot be read, ", e)


