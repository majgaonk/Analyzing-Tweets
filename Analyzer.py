from DataStorage import DataStorageInterface
import pandas as pd
import itertools
import collections
import re
import nltk
from nltk.corpus import stopwords

class TweetAnalyzer(object):

    def __init__ (self, dataStore):
        self.dataStore = dataStore

    def analyzeTweetText (self):
        df_tweet = self.dataStore.get_data (["text"])
        
        #remove the RT tag
        clean_tweet = self.cleanTweetText (df_tweet).applymap (str.lower)
        #print ("1: {0}". format(clean_tweet))

        words_collection = list(itertools.chain (*[text.split() for text in clean_tweet["text"]]))

        #remove the stopwords 
        words_collection = self.removeStopWords (words_collection)
        
        words_frequecy = collections.Counter (words_collection)
        
        return words_frequecy.most_common (10)

    def cleanTweetText (self, tweet_df):
        cleaned_df = tweet_df.applymap (self.removeRTTag)
        return cleaned_df

    def removeRTTag (self, text):
        new_text = "".join (re.sub("[R-Tr-t ]*@[a-zA-Z0-9]*[:]*", "", text))
        return new_text

    def removeStopWords(self, words_list):
        stop_words = set(stopwords.words('english'))

        new_words_list =[word for word in words_list if word not in stop_words]
        return new_words_list
        
        





