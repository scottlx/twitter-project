#!/usr/bin/python

''' 
Credit to: Krishanu Konar, GoogleCloudPlatform/python-docs-examples
modified by: Xun(Scott) Lin
'''
import json
import wget
import os
import sys
import glob
import io
from google.cloud import vision
from google.cloud.vision import types
import csv
import srt
import pymongo
import datetime
from pymongo import MongoClient
from datetime import timedelta



def get_tweets(username, max_tweets, api):
	## Getting Tweets from a user with the handle 'username' upto max of 'max_tweets' tweets
	last_tweet_id = 0
	num_images = 0
	try:
		raw_tweets = api.user_timeline(screen_name=username,include_rts=False,exclude_replies=True)  #exclude retweets and replies
	except Exception as e:
		print (e)
		sys.exit()
	if raw_tweets:
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
		return raw_tweets
	else:
		print('Seriously? This user did not post any tweets')
		sys.exit()

def get_URL(raw_tweets):
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
	return tweets_with_media


def downloadImages(image_url,username):
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

	for url in image_url:
		wget.download(url)
	print ('\n\nFinished Downloading.\n')

def recognizing():
	#Google vision
	os.system('mogrify -format jpg *.png') #convert png into jpg 
	print ('\n\nStart recognizing.\n')
	client = vision.ImageAnnotatorClient()
	print (os.getcwd())
	CURRENT_PATH = os.getcwd()
	relevant_path = glob.glob('*.jpg')
	image_paths = glob.glob(os.path.join(CURRENT_PATH, '*.jpg'))
	print ("Number of images: ", len(image_paths))

	subs =[]
	description=[]

	for index, file_name in enumerate(image_paths):
		with io.open(file_name, 'rb') as image_file:
			content = image_file.read()
		image = types.Image(content=content)
		response = client.label_detection(image=image)
		labels = response.label_annotations
		print(index)
		subs.append(srt.Subtitle(index=index, start=timedelta(seconds=index), end=timedelta(seconds=index+1), content=labels[0].description)) #write the first label into subtitle
		description.append(labels[0].description)
		with open("output.csv", "a") as f:
			writer = csv.writer(f)
			row=[]
			for label in labels:
				print(label.description)
				row.append(label.description)
			writer.writerow(row)                #save all the labels into csv file
		with open("subtitle.srt","w") as s:
			s.write(srt.compose(subs))
	s.close()
	f.close()
	return description,relevant_path


def mongo_save(user_name,twitter_name,twitter_id,lb,url):

	client = MongoClient('localhost',27017)

	db = client.twitter_mongodb


	post = {"user_name": user_name,
		"twitter_username": twitter_name,
		"twitter_id": twitter_id,
		"label": lb,
		"url": url,
		"time": datetime.datetime.utcnow()}
	try:
		posts = db.posts
		posts.insert_one(post).inserted_id
	except:
		raise Exception("insert document failed")



def mongo_search(field, keyword):

	client = MongoClient('localhost',27017)

	db = client.twitter_mongodb


	condition = {}
	condition['$regex'] = keyword
	filter = {}
	filter[field] = condition
	try:
		for post in db.posts.find(filter):
			print(post)
	except:
		raise Exception("Find data failed")