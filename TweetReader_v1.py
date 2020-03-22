from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import credentials

# # # # TWITTER CLIENT # # # #


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticateTwitterAap()
        self.twitterClient = API(self.auth)
        self.twitter_user = twitter_user

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
        self.authenticator = TwitterAuthenticator()

    def readTweets(self, fetched_tweets_filename, hash_tag_list):
        # Reads the credentials.py file and handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.authenticator.authenticateTwitterAap()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #


class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout and saves them to json file.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets = fetched_tweets

    def on_data(self, data):

        try:
            print(data)
            with open(self.fetched_tweets, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on data menthiod in case rate limit occurs
            return False
        print(status)


if __name__ == '__main__':

    # Authenticate using config.py and connect to Twitter Streaming API.

    hash_tag_list = ["coronavirus"]
    fetched_tweets = "tweets.json"
    tweetReader = TwitterReader()
    tweetReader.readTweets(fetched_tweets, hash_tag_list)

    twitterClient = TwitterClient('pycon')
    print(twitterClient.getTweets(1))
