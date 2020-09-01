import tweepy

def create_api():
    #insert your appropriate developer keys below
    consumer_key = "SpmKgkNv5otNcy70HnrvB6ZZo"
    consumer_secret = "4BNA5DNenSH4SI2JLIQXvwyjM3fPdL4xkKlQOgcARdHaJajXgZ"
    access_token = "738825300-KDPLSqwr3wU3pTal8TRQmnNpEzzBLrizjUubWggN"
    access_token_secret = "Kq4tFTFJ8nHwXACpC0E6mVYou3cMh8yLbHBoLQsQPfMrE"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        #logger.error("Error creating API", exc_info=True)
        print('error connecting api: ' + e)
        raise e
    #logger.info("API created")
    return api

class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        
        #list of words to identify dan or hayley
        dan_words = ['team_dan', 'teamdan', 'dandaggerdick', 'dan']
        hayley_words = ['hayley', 'cyrilswhore']
        print("processing tweet id: " + str(tweet.id))
        
        #tweet should contain one reference to dan AND one reference to Hayley
        if any(word in tweet.text.lower() for word in dan_words) and any(word in tweet.text.lower() for word in hayley_words): 
            print('Contains hayley and dan: ', tweet.text)

            #tweet is from account retweeting, therefore do not retweet
            if tweet.user.id == self.me.id:
                return
            
            # Retweet, since we have not retweeted it yet
            if not tweet.retweeted: 
                try:
                    tweet.retweet()
                except Exception as e:
                    print('error retweeting id: ' + e)

    def on_error(self, status):
        print('error while processing tweet')

def main():
    api = create_api()
    tweets_listener = RetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    #filter for tweets that contain at least one of your handles
    stream.filter(track=["DanDaggerDick", "Cyrilswhore"])

if __name__ == "__main__":
    main()
