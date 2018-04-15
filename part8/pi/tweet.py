import tweepy


TOKEN = "859459534405992450-8PYeAetQAT9ByhVeRlDt9vbMijpMKjY"
TOKEN_SEC = "amK3zmimfd2NGmAtFP9qxU56PVctRHq4UdKvbOMb8p5WW"
CON_KEY = "eL3Qg85y4BKy1KfXMNU3j6Ec3"
CON_SEC = "sxDh3a5YNzP8Nnf0FBC0WM8fR6IKrURpUPR1WagOyZDrBHpQok"

def tweet(image, text):
	auth = tweepy.OAuthHandler(CON_KEY,CON_SEC)
	auth.set_access_token(TOKEN,TOKEN_SEC)
	api = tweepy.API(auth)
	api.update_with_media(image, status=text)
