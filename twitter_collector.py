#!/usr/local/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler,AppAuthHandler
from tweepy import Stream, API, Cursor
from tweepy.error import TweepError
import json
import sys
import os
import time

#Variables that contains the user credentials to access Twitter API 
access_token =  os.environ["access_token"]if "access_token" in os.environ else "852983328818905088-wwBZvVWNgplvEuW5ImotWXE9ztrsL43"
access_token_secret = os.environ["access_token_secret"]if "access_token" in os.environ else"rtzbU3vh1fHqNdbHqc6DbEahGVGrVr4yMFEAOIXvXasfU"
consumer_key = os.environ["consumer_key"]if "access_token" in os.environ else"en7howoltmBGRiv0WsPka4SmE"
consumer_secret = os.environ["consumer_secret"]if "access_token" in os.environ else"PH0xSeUdk9DyDoFfzSogtygK8iuoRI5FbD9eZOxhARWV1Dxu2W"


print("using {} \n {} \n {} \n {} \n".format(access_token, access_token_secret, consumer_key, consumer_secret ))

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (json.loads(data)["text"])
        with open(r'stdout_1.json','a') as tf:
            tf.write(data)
        return True

    def on_error(self, status):
        print (status)

def collect_tweets():
         #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = AppAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    api = API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    keywords = ['#phoneless', '#no-phone', '#nophone', 'phoneless', 'nophone','"lost communication"','"no communication"','"no internet"','"no signal"','"nomophobia"','"phubbing"', '"mobile addiction"', '"Ringxiety"','"textaphrenia"', '"Phantom Ringing"','"Phantom Vibration"','Communifaking']
    maxtweets=100000
    tweetsperQry=100
    sinceID=None
    max_id=-1
    tweetCount=0
    if len(sys.argv[2:]) != 0:
        keywords_s = " OR ".join(sys.argv[2:])
        keywords_f = sys.argv[2:]
    else:
        keywords_s = " OR ".join(keywords)
        keywords_f = keywords

    #This line search Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    if sys.argv[1]=='s' or sys.argv[1]=='search':
        data = api.rate_limit_status()
        print("limit", data['resources']['search'])
        with open("results_{}.csv".format(abs(max_id)), "a") as fd:
            while tweetCount<maxtweets:
                tweets=""
                try:
                    if (max_id<=0):
                        search_results =api.search(q=keywords_s,tweet_mode="extended",lang="en",count=tweetsperQry)
                    else:
                        search_results= api.search(q=keywords_s, tweet_mode="extended", lang="en", count=tweetsperQry,max_id=str(max_id - 1))
                    for tweet in search_results:
                        #print("$$$$$$$$$$$",tweet.full_text)
                        if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                            #print("***********************************without RT",tweet.full_text.replace("\r\n", "").replace("\n", "") + "\n")
                            tweets = tweets + tweet.full_text.replace("\r\n", "").replace("\n", "") + "\n"
                    data = api.rate_limit_status()
                    #print("????????????????/limit",data['resources']['search'])
                    tweetCount += len(search_results)
                    #print(")))))))))))",tweetCount)
                    #break
                    max_id = search_results[-1].id
                    #print(tweets)
                    fd.write(tweets)
                except TypeError as e:
                    print(e)
                    print("stopped at {}".format(max_id))
                except Exception as e:
                    print(e)
                    print("stopped at {}".format(max_id))
                except KeyboardInterrupt as e:
                    print("stopped at {}".format(max_id))
                    sys.exit()

    elif sys.argv[1]=='f'or sys.argv[1]=='filter':
         #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(languages=["en"],track=keywords_f)

if __name__ == '__main__':
    collect_tweets()

