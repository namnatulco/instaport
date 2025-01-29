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
    fp = open("/cache/" + shortcode, "rb")
    # open success -> read cache file
    # TODO avoid DoS due to huge files
    contents = pickle.load(fp)
    fp.close()
    print("loaded from cache:",contents)
except FileNotFoundError:
    try:
        fp = open("/cache/" + shortcode, "wb")
        import scrape
        # return instaloader post object - use for testing only!
        contents = scrape.do_scrape(shortcode)
        pickle.dump(contents, fp)
        fp.close()
        print("wrote to cache",contents)
    except OSError as e:
        print("Error while creating cache file", e)
except OSError as e:
    print("Cache file exists but cannot be read, ", e)


