#!/usr/bin/python3
#coding=utf-8

import pymysql

# Open database connection
db = pymysql.connect("localhost","scott","445566","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

max = 'gg'
# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO employee(FIRST_NAME, \
   LAST_NAME, AGE, SEX, INCOME) \
   VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
   (max, 'Su', 25, 'F', 2800)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
