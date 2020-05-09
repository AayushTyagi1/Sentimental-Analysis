# Aayush Tyagi 2013206
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user


    def get_twitter_client_api(self):
        return self.twitter_client
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
         
# # # # Twitter Authenticater # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth= OAuthHandler(twitter_credentials.API_key,twitter_credentials.API_secret_key)
        auth.set_access_token(twitter_credentials.Access_token, twitter_credentials.Access_token_secret)
        return auth


class TwitterStreamer():
    #Class for streaming and processing live tweets
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    def stream_tweets(self, fetched_tweets_filename,hash_tag_list):
        # this handles twitter authentication and connection to API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        
        #to capture data by the keyword
        stream.filter(track=hash_tag_list)
            
             
            
class TwitterListener(StreamListener):
    #print received tweets to stdout
    def __int__(self, fetched_tweets_filename):
        self.fetched_tweets_filename= fetched_tweets_filename


    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'dataset') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on the data: %s"%str( e)) 
        return True
    
    def on_error(self,status):
        if status == 420:
            return False
        print(status)
        
if __name__ == "__main__":
    
    hash_tag_list=["Narendra Modi","Arvind kejriwal","Rahul Gandhi","Yogi Adityanath"]
    fetched_tweets_filename = "tweets.txt"
    
    twitter_client = TwitterClient("pycon")
    print(twitter_client.get_user_timeline_tweets(1))
    
 #   TwitterStreamer = TwitterStreamer()
  #  TwitterStreamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
    
