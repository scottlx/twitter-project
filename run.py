#!/usr/bin/python

import os
import sys
import tweets_converter
import tweepy
from tweepy import OAuthHandler

consumer_key = 'JJLhC7QSHGmNJlVexDnNuCXY2'
consumer_secret = '54xkXLWXQDTc89kv0RnGvfWcFJPIezaMUQWYrZ6MrZZyVempsb'
access_token = '1038838122061160455-HWxQ4alHDV1qgzRwuropLKM6Qb4XtV'
access_secret = '6O7T5jIGnTjD4ibeJM43jePp8ru6lkMDLJzDIKMeTXAlW'

#Authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


while True:
	myname = input("\nEnter your name: ")
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
	label,paths = tweets_converter.recognizing()
	i=0
	for lb in label:
		url= 'http://pbs.twimg.com/media/'+paths[i]
		i=i+1
		tweets_converter.mongo_save(myname,u.screen_name,u.id_str,lb,url)
	# use ffmpeg command to convert the images and subtitle into a video
	os.system('ffmpeg -framerate 1 -pattern_type glob -i \'*.jpg\' -vf \"scale=\'min(1280,iw)\':min\'(720,ih)\':force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2 , subtitles=subtitle.srt\" output.mp4')

else:
	print('No images in the twitter feed')
	sys.exit()


field = input("\nEnter the Field (user_name, twitter_username, twitter_id, label, url, time) you want to search: ")
keyword = input("\nEnter the searching keyword: ")
tweets_converter.mongo_search(field, keyword)