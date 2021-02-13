from dotenv import load_dotenv
import praw
import os

load_dotenv()

# KEYS
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_SECRET')
USERNAME = os.environ.get('user')
PASSWORD = os.environ.get('pass')

reddit = praw.Reddit(client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET,
                   username=USERNAME,
                   password=PASSWORD,
                   user_agent='hackathon',
                   redirect_uri='http://localhost:8080')
print(reddit.auth.url(["identity"], "...", "permanent"))

subreddit = reddit.subreddit("python")

hot_python = subreddit.hot(limit=5)

for submission in hot_python:
    print(submission.title)
