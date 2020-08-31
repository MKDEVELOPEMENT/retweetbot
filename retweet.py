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
        print('error here')
        raise e
    #logger.info("API created")
    return api

class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print("Processing tweet id " + tweet.id)
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or you are its author so, ignore it
            return
        if not tweet.retweeted:
            #insert your own keyword in here to replace "test1"
            if 'test1' in tweet.text:
                try:
                    # Retweet, since we have not retweeted it yet
                    tweet.retweet()
                except Exception as e:
                    print('error retweeting')

    def on_error(self, status):
        print('error')

def main(keywords):
    api = create_api()
    tweets_listener = RetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    #set the follow number to the user ID of the user you want to track
    stream.filter(follow=['1285625854714957832'], 
                           track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["test1"])
