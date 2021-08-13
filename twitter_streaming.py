from DataStorage import InMemoryDataStorage
from DataExtractor import DataExtractor
from Analyzer import TweetAnalyzer
import os
import tweepy
import json
import pandas as pd
import matplotlib.pyplot as plt

class MyStreamListener (tweepy.StreamListener):
    def __init__ (self, num_tweets_to_get, dataStore):
        tweepy.StreamListener.__init__(self)
        self.num_tweets_to_get = num_tweets_to_get
        self.tweet_count = 0
        self.dataStore = dataStore
    
    #def on_status (self, status):
    #    print ("Status : {0}". format (type (status)))
    #    print (status)
    #   self.tweet_count += 1
    #   if self.tweet_count >= num_tweets_to_get:
    #       return False
    #   return True

    def on_data (self, data):
        
        self.store_data (data)
        self.tweet_count += 1

        if self.tweet_count >= num_tweets_to_get:
            return False
        return True

    def store_data (self, data):
        json_data = json.loads (data)
        self.dataStore.store_data (json_data)
    
    




def  create_api_credentials ():
    # Authenticate to Twitter
    CONSUMER_KEY = os.getenv ("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv ("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv ("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv ("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        print("Authentication Success")
        return auth
    except Exception as err:
        raise err

    return None

if __name__ == "__main__":
    num_tweets_to_get = 1000 

    try:      
        auth = create_api_credentials()
        dataExtractor = DataExtractor()
        dataStore = InMemoryDataStorage (dataExtractor)
        streamListener = MyStreamListener (num_tweets_to_get, dataStore)
        print ("Fetching Data from Twitter")
        myStream = tweepy.Stream(auth = auth, listener=streamListener)
        myStream.filter(track=['covid-19', 'covid'], languages=["en"])

        print ("Analyzing")
        analyzer = TweetAnalyzer (dataStore)
        plot_data = analyzer.analyzeTweetText()

        #plot the top 15 word counts
        print ("Plotting")
        plot_df = pd.DataFrame (plot_data, columns=["words", "count"])
        plot_df.sort_values(by="count").plot(kind="bar", x="words", y="count", color="blue", title="Top word counts in analyzed tweets")

        plt.show()

    except Exception as err:
        print("Unexpected error: {0}".format (err))

    
