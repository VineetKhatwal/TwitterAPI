from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import numpy as np
import pandas as pd
import csv
import ast
import credentials

# # # # TWITTER CLIENT # # # #

tweets = []


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticateTwitterAap()
        self.twitterClient = API(self.auth)
        self.twitter_user = twitter_user

    def getTwitterClientApi(self):
        return self.twitterClient

    def getTweets(self, numTweets):
        tweets = []
        for tweet in Cursor(self.twitterClient.user_timeline, id=self.twitter_user).items(numTweets):
            tweets.append(tweet)
        return tweets

    def getFriendList(self, numFriends):
        friendList = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(numFriends):
            friendList.append(friend)
        return friendList

    def getHomeTimelineTweets(self, numTweets):
        homeTimelineTweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(numTweets):
            homeTimelineTweets.append(tweet)
        return homeTimelineTweets


# # # # TWITTER AUTHENTICATOR # # # #


class TwitterAuthenticator():

    def authenticateTwitterAap(self):
        auth = OAuthHandler(credentials.CONSUMER_API_KEY,
                            credentials.CONSUMER_API_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN,
                              credentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWEET READER # # # #


class TwitterReader():

    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.auth = TwitterAuthenticator().authenticateTwitterAap()
        self.twitterClient = API(self.auth)

    def getTwitterClientApi(self):
        return self.twitterClient

    def readTweets(self, fetched_tweets_filename, hash_tag_list, numTweets):
        # Reads the credentials.py file and handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename, numTweets)
        # auth = self.authenticator.authenticateTwitterAap()
        stream = Stream(self.auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #


class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout and saves them to json file.
    """

    def __init__(self, fetched_tweets_filename, numTweets):
        self.fileName = fetched_tweets_filename
        self.numTweets = numTweets
        self.tweetCount = 0

    def on_data(self, data):

        global tweets

        try:
            self.tweetCount += 1
            # print(self.tweetCount, self.numTweets, self.fileName)
            if(self.tweetCount > self.numTweets):
                print("completed")
                return(False)
            else:
                # print(data)
                data = data.replace("true", "True")
                data = data.replace("false", "False")
                data = data.replace("null", "None")
                temp = eval(data)
                # print(type(temp))
                # tweets += data
                tweets.append(temp)
                # with open(self.fileName, 'a') as tf:
                # tf.write(temp)
                # return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on data menthiod in case rate limit occurs
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def flatten_json(y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '.')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '.')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def tweetsToDataFrame(self, tweets):
        '''
        for i in tweets:
            res = TweetAnalyzer.flatten_json(i)
        '''

        column_names = ["created_at", "text", "id", "id_str",
                        "source", "user", "reply_count", "retweet_count"]
        list = []
        df = pd.DataFrame(
            data=[tweet for tweet in tweets], columns=['Tweets'])
        for i in tweets:
            # print(i['text'])
            list.append([i['created_at'], i['text'], i['id'], i['id_str'],
                         i['source'], i['user'], i['reply_count'], i['retweet_count']])
        df = pd.DataFrame(list, columns=column_names)
        '''
            df['created_at'] = np.array(i['created_at'])
            df['text'] = np.array(i['text'])
            df['id'] = np.array(i['id'])
            df['id_str'] = np.array(i['id_str'])
            df['source'] = np.array(i['source'])
            df['user'] = np.array(i['user'])
            df['reply_count'] = np.array(i['reply_count'])
            df['retweet_count'] = np.array(i['retweet_count'])
        '''
        # df['date'] = np.array([tweet.created_at for tweet in tweets])

        return df


if __name__ == '__main__':

    # Authenticate using config.py and connect to Twitter Streaming API.

    hash_tag_list = ["coronavirus"]
    fileName = "tweets.json"
    tweetReader = TwitterReader()
    tweet_analyzer = TweetAnalyzer()

    tweetReader.readTweets(fileName, hash_tag_list, 7)
    # print("=====================================================")
    # print(tweets)
    # print(dir(tweets[0]))
    df = tweet_analyzer.tweetsToDataFrame(tweets)
    df.to_csv("Tweets.csv", encoding='utf-8', index=False)

    # print(df)

    # **********************************************************************************
    #
    #                                   FOR GETTING A USER TWEET
    #
    # **********************************************************************************

    # twitterClient = TwitterClient('pycon')
    # print(twitterClient.getTweets(2))
