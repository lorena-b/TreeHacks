"""
SENTIMENT FUNCTIONS
"""
import auth
from praw.models import MoreComments
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from pprint import pprint

nltk.download('vader_lexicon')
sia = SIA()

# INSTANCES AND CONSTANTS
reddit = auth.reddit
GATHER_LIMIT = 5  # max amount of posts to gather

# SAMPLE CODE FOR REFERENCE
# subreddit = reddit.subreddit("python")
#
# hot_python = subreddit.hot(limit=5)
#
# for submission in hot_python:
#     if not submission.stickied:
#         print(f'Title: {submission.title}, \n\
#                 Upvotes: {submission.ups}, \n\
#                 Downvotes: {submission.downs}, \n\
#                 Visited: {submission.visited}'
#               )
#     comments = submission.comments.list()
#     for comment in comments:
#         print(20 * '-')
#         print(comment.body)
#         print('PARENT ID: ', comment.parent())  # API CALL
#         print('COMMENT ID: ', comment.id)  # ATTRIBUTE
#         if len(comment.replies) > 0:
#             for reply in comment.replies:
#                 print('REPLY:', reply.body)


def get_posts(topic: str) -> dict[int, dict]:
    """Return the hot <GATHER_LIMIT> posts associated with an input topic
    :return: JSON format
    """
    # posts in r/all
    all_reddit = reddit.subreddit("all")
    posts = {}

    count = 0
    for post in all_reddit.search(topic, sort='hot', limit=GATHER_LIMIT):
        if not post.stickied and post.comments is not None:
            posts[count] = {
                'name': post.title,
                'subreddit': post.subreddit,
                'text': post.selftext,
                'comments': comments_to_str(post)
            }
            count += 1

    return posts


def comments_to_str(submission) -> list[str]:
    """Extract the comment body from comment list

    :return: str
    """
    new_list = []
    comments = submission.comments.list()
    for comment in comments:
        if not isinstance(comment, MoreComments):
            new_list.append(comment.body)

    return new_list


def get_sentiment(comments) -> any:
    """Return sentiment for a POST (based on comments)
    """
    results = []
    for line in comments:
        pol_score = sia.polarity_scores(line)
        pol_score['comment'] = line
        results.append(pol_score)

    return results


def sentiment_manager(topic: str) -> any:
    """Return the SENTIMENT REPORT for the whole topic (this will be called
    by the API)
    """
    # average sentiment is the sum of all post sentiment / gather limit
    sent_report = {}
    test = []
    posts = get_posts(topic=topic)
    for i in range(len(posts)):
        post_sent = get_sentiment(posts[i]['comments'])
        test.append(post_sent)

    return test

