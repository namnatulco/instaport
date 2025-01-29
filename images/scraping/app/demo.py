import instaloader
from sys import argv

if len(argv) != 2 or not argv[1] or len(argv[1]) != 11:
    print("Error, provide exactly one shortcode as argument (shortcodes have a length of 11 chars)")
    if(argv[1]):
        print("provided first argument is:",argv[1])
    exit(1)

shortcode=argv[1]

L = instaloader.Instaloader()

post = instaloader.Post.from_shortcode(L.context, shortcode)
print("posted on:", post.date)
print("posted by:", post.owner_username)
print("post title:", post.title)
print("post thumb url:", post.url)
print("post caption:", post.caption)
if post.location:
    print("location associated with the post:",post.location)

