import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from googletrans import Translator
import matplotlib.pyplot as plt

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    
    '''
    x_axis=['neg','neu','pos']
    y_axis=[0,0,0]
    scatter_x=[]
    scatter_y=[]
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = '4ZxLjoXxV5dIZAmfmUWZWqT9i'
        consumer_secret = 'RIY3gxKtQiTIs87MmqShBHixd1jdaIiHR18pZc2xZMv3U9WXsg'
        access_token = '1339638829607657472-lfx713UxZgxsH9OxBVzyKDKDe19UFJ'
        access_token_secret = 'pxSINy8RJ7Mcs3E9yHcWXPqRBjJaQigMJIfNyK3lySNdF'
        
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, 
                                     consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, 
                                       access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, 
        special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            self.y_axis[2]+=1
            self.scatter_x.append(int(analysis.sentiment.polarity))
            self.scatter_y.append('pos')
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            self.y_axis[1]+=1
            self.scatter_x.append(int(analysis.sentiment.polarity))
            self.scatter_y.append('neu')
            return 'neutral'
        else:
            self.y_axis[0]+=1
            self.scatter_x.append(int(analysis.sentiment.polarity))
            self.scatter_y.append('neg')
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        translator=Translator()
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query,
                                             count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                
                #Bilangual Translation to english
                sent=tweet.text
                sent=str(sent.encode('unicode-escape').decode('ASCII'))
                translations = translator.translate(sent,dest="en")
                transtweets=translations.text
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] =  transtweets
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(transtweets)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def plotgraph(self):
        bar_graph=plt.figure(1)
        plt.bar(self.x_axis,self.y_axis)
        scatter_plot=plt.figure(2)
        plt.scatter(self.scatter_x,self.scatter_y)

        plt.title("Twitter Sentiment Analysis")
        plt.show()


def main(tweeterhandle):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = tweeterhandle, count = 200)
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] 
               == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %"
          .format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if 
               tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    #print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} % \
    #    ".format(100*len(tweets - ntweets - ptweets)/len(tweets)))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
    #calling graph function    
    api.plotgraph()

if __name__ == "__main__":
    main()