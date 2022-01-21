import tweepy
from bs4 import BeautifulSoup
import requests
import os
import time
from keep_alive import keep_alive

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
key = os.environ['KEY']
secret = os.environ['SECRET']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

keep_alive()

def glamBot():
    url = "https://ffxiv.eorzeacollection.com/glamours"

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    for link in doc.find_all('a', class_ = "c-glamour-grid-item-link")[:1]:
        href = link.get("href")
        sets = "ffxiv.eorzeacollection.com" + href
    
    for title in doc.find_all(class_ = "c-glamour-grid-item-content-title")[:1]:
        setName = title.string

    for name in doc.find_all('h4', class_ = "c-glamour-grid-item-content-author")[:1]:
        child = name.findChild('b')
        author = child.string

    tweet = "❗New Glamour❕\n" + '✨ "' + setName + '" ✨\n' + "◽ by " + author + " ◽\n " + sets
    return tweet


def get_last_tweet():
    last_tweet = api.user_timeline(count = 200, include_rts = False)[0]
    return last_tweet.text.encode("utf-8")

def retweetBot(hashtag):
    for tweet in tweepy.Cursor(api.search_tweets, q=hashtag, count = 10).items(5):
        try:
            tweet_id = dict(tweet._json)['id']

            api.retweet(tweet_id)
            print('Tweet retweeted')

        except tweepy.TweepyException as error:
            print(error)
        

get_last_tweet()
glamBot()


while(True):
    
    if get_last_tweet()[0:50] != glamBot().encode("utf-8")[0:50]:      
        print(get_last_tweet()[0:50])
        print(glamBot().encode("utf-8")[0:50])
        try:
            retweetBot('#GPOSERS')
            api.update_status(glamBot())
            print('Tweet Sent.')
        except:
            print('Duplicate')
    else:
        print('Duplicate tweet')
        time.sleep(10)

