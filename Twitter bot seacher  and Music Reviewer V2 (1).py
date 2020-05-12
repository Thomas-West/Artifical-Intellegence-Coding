#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tweepy
import csv
import ssl
import time
from tweepy import Stream, StreamListener, OAuthHandler
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError

# Add your Twitter API credentials
consumer_key = "CNS18gUCgMqbMcuP0O88uLOfy"
consumer_secret = "ewqfl0jruElVFEy0uGkZLH118LFbGQxIfqi4V9dNzaoKhelsGY"
access_key = "749662970658033664-2CzHlLY2VmoiEX871w1rlCrs5kimPcp"
access_secret = "pU2UosrAa6n9GRK1ubjb02n5OWKgmd8LVPkrGF6PEvUSu"

# Handling authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create a wrapper for the API provided by Twitter
api = tweepy.API(auth,wait_on_rate_limit=True)

# Setting up the keywords, hashtag or mentions we want to listen
keywords = ["#music", "music", "music review", "song", "album"] 

# Set the name for CSV file  where the tweets will be saved
filename = "musicreview"



#get myStream to sync up with Streamlistener and prepare a filter
myStream = tweepy.Stream(auth = api.auth, listener=StreamListener())


# We need to implement StreamListener to use Tweepy to listen to Twitter
class StreamListener(tweepy.StreamListener):

    tweet_counter = 0 # Static variable and counter of how many tweet downloaded

    
    def on_status(self, status):

        try:
            # saves the tweet object
            tweet_object = status

            # Checks if its a extended tweet (>140 characters)
            if 'extended_tweet' in tweet_object._json:
                tweet = tweet_object.extended_tweet['full_text']
            else:
                tweet = tweet_object.text
                

            # Save the keyword that matches the stream
            keyword_matches = []
            for word in keywords:
                if word.lower() in tweet.lower():
                    keyword_matches.extend([word])

            keywords_strings = ", ".join(str(x) for x in keyword_matches)

            # Save other information from the tweet
            user = status.author.screen_name
            timeTweet = status.created_at
            source = status.source
            tweetId = status.id
            tweetUrl = "https://twitter.com/statuses/" + str(tweetId)

            # Exclude retweets, too many mentions and too many hashtags
            if not any((('RT @' in tweet, 'RT' in tweet,
                       tweet.count('@') >= 2, tweet.count('#') >= 3))):

                # Saves the tweet information in a new row of the CSV file
                writer.writerow([tweet, keywords_strings, timeTweet,
                                user, source, tweetId, tweetUrl])

        except Exception as e:
            print('Encountered Exception:', e)
            pass

        
        StreamListener.tweet_counter += 1
        print(str(StreamListener.tweet_counter) + " Tweet has been found      :"  +  str(tweet))
        
        
        
        if self.tweet_counter < 100:
            return True
        else:
            return False
        
def filter(self, follow=None, track=None, is_async=False, locations=None,
               stall_warnings=False, languages=None, encoding='UTF-8', filter_level=None):

    def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')


def work():

    # Opening a CSV file to save the gathered tweets
    with open(filename+".csv", 'w', encoding="UTF-8") as file:
        global writer
        writer = csv.writer(file)

        # Add a header row to the CSV
        writer.writerow(["Tweet", "Matched Keywords", "Date", "User",
                        "Source", "Tweet ID", "Tweet URL"])

        # Initializing the twitter streap Stream
        try:
            streamingAPI = tweepy.streaming.Stream(auth, StreamListener())
            streamingAPI.filter(track=keywords)

        # Stop temporarily when hitting Twitter rate Limit
        except tweepy.RateLimitError:
            print("RateLimitError...waiting ~15 minutes to continue")
            time.sleep(1001)
            streamingAPI = tweepy.streaming.Stream(auth, StreamListener())
            streamingAPI.filter(track=[keywords])

        # Stop temporarily when getting a timeout or connection error
        except (Timeout, ssl.SSLError, ReadTimeoutError,
                ConnectionError) as exc:
            print("Timeout/connection error...waiting ~15 minutes to continue")
            time.sleep(1001)
            streamingAPI = tweepy.streaming.Stream(auth, StreamListener())
            streamingAPI.filter(track=[keywords])

        # Stop temporarily when getting other errors
        except tweepy.TweepError as e:
            if 'Failed to send request:' in e.reason:
                print("Time out error caught.")
                time.sleep(1001)
                streamingAPI = tweepy.streaming.Stream(auth, StreamListener())
                streamingAPI.filter(track=[keywords])
            else:
                print("Other error with this user...passing")
                pass


if __name__ == '__main__':

    work()


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import nltk


# In[ ]:


from pathlib import Path


# In[ ]:


from textblob import TextBlob


# In[ ]:


blob = TextBlob(Path('musicreview.csv').read_text(encoding="UTF-8"))


# In[ ]:


blob.sentiment


# In[ ]:


from nltk.corpus import stopwords


# In[ ]:


stop_words = stopwords.words('english')
stop_words.append('“')
stop_words.append('”')
stop_words.append("twitter")
stop_words.append('’')
stop_words.append('https')
stop_words.append('—')
stop_words.append('2020-05-12')


# In[ ]:


items = blob.word_counts.items()


# In[ ]:


items = [item for item in items if item[0] not in stop_words]


# In[ ]:


from operator import itemgetter


# In[ ]:


sorted_items = sorted(items, key=itemgetter(1), reverse=True)


# In[ ]:


top20 = sorted_items[1:21]


# In[ ]:


import pandas as pd


# In[ ]:


df = pd.read_csv('musicreview.csv', sep=',\s+', delimiter=',', encoding="UTF-8", skipinitialspace=True)


# In[ ]:


df = pd.DataFrame(top20, columns=['word', 'count'])  


# In[ ]:


df


# In[ ]:


axes = df.plot.bar(x='word', y='count', legend=False)

import matplotlib.pyplot as plt

plt.gcf().tight_layout()

