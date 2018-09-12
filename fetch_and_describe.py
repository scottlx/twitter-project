#!/usr/bin/python

''' 
Credit to: Krishanu Konar, GoogleCloudPlatform/python-docs-examples
modified by: Xun(Scott) Lin
'''
import tweepy
from tweepy import OAuthHandler
import json
import wget
import os
import sys
import glob
import io
from google.cloud import vision
from google.cloud.vision import types
import csv

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

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

## Getting Tweets from a user with the handle 'username' upto max of 'max_tweets' tweets
last_tweet_id = 0
num_images = 0
try:
    raw_tweets = api.user_timeline(screen_name=username,include_rts=False,exclude_replies=True)  #exclude retweets and replies
except Exception as e:
	print (e)
	sys.exit()

last_tweet_id = int(raw_tweets[-1].id-1)
	
print ('\nFetching tweets.....')

if max_tweets == 0:
	max_tweets = 3500   #if max_tweets is 0, fetch all tweets

while len(raw_tweets)<max_tweets:
	sys.stdout.write("\rTweets fetched: %d" % len(raw_tweets))
	sys.stdout.flush()
	temp_raw_tweets = api.user_timeline(screen_name=username, max_id=last_tweet_id, include_rts=False, exclude_replies=True)  #read the timeline relative to max_id (the IDs of Tweets it has already processed)

	if len(temp_raw_tweets) == 0:
		break
	else:
		last_tweet_id = int(temp_raw_tweets[-1].id-1)
		raw_tweets = raw_tweets + temp_raw_tweets

print ('\nFinished fetching ' + str(min(len(raw_tweets),max_tweets)) + ' Tweets.')


#obtaining the full path for the images in raw_tweets
print ('\nCollecting Media URLs.....')
tweets_with_media = set()
for tweet in raw_tweets:
	media = tweet.entities.get('media',[])
	if (len(media)>0):
		tweets_with_media.add(media[0]['media_url'])
		sys.stdout.write("\rMedia Links fetched: %d" % len(tweets_with_media))
		sys.stdout.flush()
print ('\nFinished fetching ' + str(len(tweets_with_media)) + ' Links.')



#Download the images into /twitter_images/"username"
print ('\nDownloading Images.....')
try:
    os.mkdir('twitter_images')
    os.chdir('twitter_images')
except:
	os.chdir('twitter_images')

try:
    os.mkdir(username)
    os.chdir(username)
except:
	os.chdir(username)

for url in tweets_with_media:
	wget.download(url)
print ('\n\nFinished Downloading.\n')


#Google vision
print ('\n\nStart recognizing.\n')
client = vision.ImageAnnotatorClient()
print (os.getcwd())
CURRENT_PATH = os.getcwd()
image_paths = glob.glob(os.path.join(CURRENT_PATH, '*.jpg'))
image_paths.sort()
print ("Number of images: ", len(image_paths));

for index, file_name in enumerate(image_paths):
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()
	image = types.Image(content=content)
	response = client.label_detection(image=image)
	labels = response.label_annotations
	print(index)
	with open("output.csv", "a") as f:
		writer = csv.writer(f)
		row=[]
		for label in labels:
			print(label.description)
			row.append(label.description)
		writer.writerow(row)
f.close()