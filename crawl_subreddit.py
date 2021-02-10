from classes.PostCrawler import *
from constants import *
import praw, sys

vals = [sys.argv[1], "hot", "all"]
if len(sys.argv) > 2:
    vals[1] = sys.argv[2]
if len(sys.argv) > 3:
    vals[2] = sys.argv[3]

reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret,
                     user_agent=user_agent,
                     username=username,
                     password=pswd)

pc = PostCrawler(reddit, vals[0])
pc.crawl(method=vals[1], period=vals[2])
pc.compile_all()
print("Done")
