from flask import Flask, jsonify, request, render_template  
from dotenv import load_dotenv 
import tweepy
import os  

# LOAD KEYS 
load_dotenv(".env", verbose=True)
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

app = Flask(__name__)

@app.route('/')
def index():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    search = request.args.get('q')
    public_tweets = api.user_timeline(search)

    return render_template('index.html', tweets=public_tweets)

@app.route('/getdata', methods=['GET'])    
def get_data():
    return jsonify({'test': 'random test json'})

if __name__ == '__main__':
    app.run(debug=True)