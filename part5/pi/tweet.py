import tweepy

TOKEN = "XXX"
TOKEN_SEC = "XXX"
CON_KEY = "XXX"
CON_SEC = "XXX"

def tweet(image, text):
	auth = tweepy.OAuthHandler(CON_KEY,CON_SEC)
	auth.set_access_token(TOKEN,TOKEN_SEC)
	api = tweepy.API(auth)
	api.update_with_media(image, status=text)
