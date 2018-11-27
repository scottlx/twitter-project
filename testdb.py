#!/usr/bin/python3
#coding=utf-8

import pymysql
import datetime

db = pymysql.connect("localhost","scott","445566","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

keyword = "lac"
sql = 'SELECT * FROM TwitterRecord WHERE ( user_name LIKE "%{}%"'.format(keyword)+'OR twitter_username LIKE "%{}%"'.format(keyword) +'OR twitter_id LIKE "%{}%"'.format(keyword) +'OR label LIKE "%{}%"'.format(keyword)+'OR url LIKE "%{}%"'.format(keyword) +'OR time LIKE "%{}%")'.format(keyword)
try:
  cursor.execute(sql)
  # Fetch all the rows in a list of lists.
  results = cursor.fetchall()
  for row in results:
    print (row)
except:
  import traceback
  traceback.print_exc()
  print ("Error: unable to fetch data")

# disconnect from server
db.close()