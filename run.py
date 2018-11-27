#!/usr/bin/python

import os
import sys
import tweets_converter
import tweepy
from tweepy import OAuthHandler

consumer_key = 'Mhi0eHP1VHR7kbFeW5jaWPZvQ'
consumer_secret = '6kX1Hz743Kw0pEYsluU4AJzBKEqJofl4Ay7u36bLUfB1b3gxzJ'
access_token = '1038838122061160455-n67qK1qNV8yjtYkEpSDclKCfhoIpHF'
access_secret = 'HyFxExkSw7VvCh4zR249eBJChbCBPMwvy6wE3jxhLcIpz'

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
	lable,paths = tweets_converter.recognizing()
	i=0
	for lb in lable:
		url= 'http://pbs.twimg.com/media/'+paths[i]
		i=i+1
		tweets_converter.mysql_save(myname,u.screen_name,u.id_str,lb,url)
	# use ffmpeg command to convert the images and subtitle into a video
	os.system('ffmpeg -framerate 1 -pattern_type glob -i \'*.jpg\' -vf \"scale=\'min(1280,iw)\':min\'(720,ih)\':force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2 , subtitles=subtitle.srt\" output.mp4')

else:
	print('No images in the twitter feed')
	sys.exit()

keyword = input("\nEnter the keyword you want to search: ")
tweets_converter.mysql_search(keyword)

