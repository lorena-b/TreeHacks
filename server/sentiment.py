"""
SENTIMENT FUNCTIONS
"""
import auth
from praw.models import MoreComments
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


nltk.download('vader_lexicon')
sia = SIA()

# INSTANCES AND CONSTANTS
reddit = auth.reddit
GATHER_LIMIT = 50  # max amount of posts to gather


def get_posts(topic: str) -> dict[int, dict]:
    """Return the hot <GATHER_LIMIT> posts associated with an input topic

    :return: dictionary with keys as the post number and then the value is a dictionary
    containing the post information
    """
    # posts in r/all
    all_reddit = reddit.subreddit("all")
    posts = {}

    count = 0
    for post in all_reddit.search(topic, sort='hot', limit=GATHER_LIMIT):
        comments = comments_to_str(post)
        if not post.stickied and len(comments) > 0:
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


def get_post_sentiment(comments) -> tuple:
    """Return sentiment for a POST (based on comments)

    results shows the polarity for EACH COMMENT
    post_score shows the average polarity for each section for the WHOLE POST
    """
    total_pos = 0
    total_neg = 0
    total_neutral = 0
    results = []
    post_score = []

    for line in comments:
        pol_score = sia.polarity_scores(line)
        pol_score['comment'] = line
        total_pos += pol_score['pos']
        total_neg += pol_score['neg']
        total_neutral += pol_score['neu']
        results.append(pol_score)

    total_pos /= len(comments)
    total_neg /= len(comments)
    total_neutral /= len(comments)

    post_score.append({
        'AVG POS': total_pos,
        'AVG NEG': total_neg,
        'AVG NEU': total_neutral
    })

    return results, post_score


def get_topic_sentiment(topic: str) -> list[dict]:
    """
    Get the overall sentiment for a topic EX: This topic is POSITIVE
    :return: report
    """

    posts = get_posts(topic=topic)

    topic_pos = 0
    topic_neg = 0
    topic_neu = 0
    sent_report = []

    for i in range(len(posts)):
        post_sent = get_post_sentiment(posts[i]['comments'])[1]
        topic_pos += post_sent[0]['AVG POS']
        topic_neg += post_sent[0]['AVG NEG']
        topic_neu += post_sent[0]['AVG NEU']

    topic_pos /= len(posts)
    topic_neg /= len(posts)
    topic_neu /= len(posts)

    if max(topic_pos, topic_neg, topic_neu) == topic_pos:
        sent = 'POSITIVE'
    elif max(topic_pos, topic_neg, topic_neu) == topic_neg:
        sent = 'NEGATIVE'
    else:
        sent = 'NEUTRAL'

    sent_report.append({
        'TOPIC POS': "{:.2%}".format(topic_pos),
        'TOPIC NEG': "{:.2%}".format(topic_neg),
        'TOPIC NEU': "{:.2%}".format(topic_neu),
        'SENTIMENT': sent,
        'VOLATILITY': (topic_pos + topic_neg) - topic_neu
    })

    return sent_report


def sentiment_report(topic: str) -> any:
    """Return the SENTIMENT REPORT for the whole topic (this will be called
    by the API)
    """
    sent_report = {
        topic: get_topic_sentiment(topic)
    }

    return sent_report
