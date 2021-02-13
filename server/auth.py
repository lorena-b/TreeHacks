from dotenv import load_dotenv
import praw 
import os 

load_dotenv()

# KEYS
CLIENT_ID= os.environ('CLIENT_ID')
CLIENT_SECRET= os.environ('REDDIT_SECRET')
USERNAME= os.environ('user')
PASSWORD= os.environ('pass')


auth = praw.Reddit(client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET,
                   username=USERNAME,
                   password=PASSWORD,
                   user_agent='hackathon')

