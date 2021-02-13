"""
Analyze trends
"""
import datetime
from datetime import date
import auth

reddit = auth.reddit

keyword = 'Trump'
GATHER_LIMIT = 50

thisdict = {
    "stocks": ["wallstreetbets", "stocks", "investing", "all", "news", "robinhood"],
    "news": ["news", "worldnews", "usnews", "politics", "todayilearned", "all"],
    "media": ["movies", "marvelstudios", "DC_Cinematic", "StarWars", "Music", "all"],
    "all": ["all"]
}

valuedicmonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0]

valuedicweek = [0, 0, 0, 0, 0, 0, 0]
today = date.today()
month = (int(f"{today:%m}"))
day = (int(f"{today:%d}"))


def monthf(keyword, subreddit, valuedic):
    subreddit = reddit.subreddit(subreddit)
    hot_python = subreddit.top('month', limit=GATHER_LIMIT)
    for submission in hot_python:
        timestamp = submission.created_utc
        value = datetime.datetime.fromtimestamp(timestamp)
        postmonth = (int(f"{value:%m}"))
        postday = (int(f"{value:%d}"))
        if keyword in submission.title:
            if postmonth == month:
                valuedic[30 - (day - postday)] += 1
            else:
                if ((postmonth == 1) or (postmonth == 3) or (postmonth == 5) or
                        (postmonth == 7) or (postmonth == 8) or
                        (postmonth == 9) or (postmonth == 10) or (postmonth == 12)):
                    valuedic[(day - 1) - (31 - postday) + 5] += 1
                elif postmonth == 2:
                    valuedic[(day - 1 - (28 - postday)) + 5] += 1
                else:
                    valuedic[(day - 1 - (30 - postday)) + 5] += 1
    return valuedic


def montharray(keyword, topic, valuedic):
    for i in (thisdict[topic]):
        valuedic = monthf(keyword, i, valuedic)
    return valuedic
