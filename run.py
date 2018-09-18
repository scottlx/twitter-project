#!/usr/bin/python

import os
import tweets_converter
import tweepy
from tweepy import OAuthHandler

consumer_key = 'ZMQLBnXbFeSeAnr3cIcI97atA'
consumer_secret = 'cUchf3TkWJdhZcSoMn63JSaf6KM7cf125HKjejpwhyGEFvha90'
access_token = '1038838122061160455-fgCTyxC6r1PPDpoZyrNphV2XhY9Y1D'
access_secret = 'IhSQL4jlSuvPfHsGjPcdu0U9mm1FTkzMlnCOwFnD6cEQD'

#Authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
username = input("\nEnter the twitter handle of the Account to download media from: ")
max_tweets = int(input("\nEnter Max. number of tweets to search (0 for all tweets): "))
#try:
#	u=api.get_user(username)
#	print (u.id_str)
#	print (u.screen_name)
#except Exception as e:
#	print (e)
#	sys.exit()
all_tweets = tweets_converter.get_tweets(username,max_tweets,api)
media_URLs = tweets_converter.get_URL(all_tweets)	
tweets_converter.downloadImages(media_URLs,username)
tweets_converter.recognizing()
# use ffmpeg command to convert the images and subtitle into a video
os.system('ffmpeg -framerate 1 -pattern_type glob -i \'*.jpg\' -vf \"scale=\'min(1280,iw)\':min\'(720,ih)\':force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2 , subtitles=subtitle.srt\" output.mp4')
