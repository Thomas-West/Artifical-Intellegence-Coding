#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tweepy
import csv
import pandas as pd
import ssl
import time
####input your credentials here
consumer_key = "CNS18gUCgMqbMcuP0O88uLOfy"
consumer_secret = "ewqfl0jruElVFEy0uGkZLH118LFbGQxIfqi4V9dNzaoKhelsGY"
access_key = "749662970658033664-2CzHlLY2VmoiEX871w1rlCrs5kimPcp"
access_secret = "pU2UosrAa6n9GRK1ubjb02n5OWKgmd8LVPkrGF6PEvUSu"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Open/Create a file to append data
csvFile = open('musictest.csv', 'a', encoding="UTF-8")
global writer

#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="#music",count=100,
                           lang="en",
                           since="2020-01-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


# In[ ]:




