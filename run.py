#!/usr/bin/python

import os
import sys
import tweets_converter
import tweepy
from tweepy import OAuthHandler

consumer_key = 'z2lLnyy4SOi2TpaBAsGVn0pty'
consumer_secret = 'wc47vwSyvNuT4HZFFoBxBMEhXmRSdsdbQcX15zNjxTKkvnc1xo'
access_token = '1038838122061160455-7KG4IXXpsMNvDy0wGPkhqMAeSyg5kT'
access_secret = 'Ez2eeD9YyFyr7iWLzfRl8uMbL7IH5lGVrg72uOPiIbfkP'

#Authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


while True:
	username = input("\nEnter the twitter handle of the Account to download media from: ")
	try:
		u=api.get_user(username)
		print (u.id_str)
		print (u.screen_name)
		break
	except Exception as e:
		print (e)

max_tweets = int(input("\nEnter Max. number of tweets to search (0 for all tweets): "))

all_tweets = tweets_converter.get_tweets(username,max_tweets,api)
media_URLs = tweets_converter.get_URL(all_tweets)
if media_URLs:
	tweets_converter.downloadImages(media_URLs,username)
	tweets_converter.recognizing()
	# use ffmpeg command to convert the images and subtitle into a video
	os.system('ffmpeg -framerate 1 -pattern_type glob -i \'*.jpg\' -vf \"scale=\'min(1280,iw)\':min\'(720,ih)\':force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2 , subtitles=subtitle.srt\" output.mp4')

else:
	print('No images in the twitter feed')
	sys.exit()

