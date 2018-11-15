#!/usr/bin/env python3
#
#Author: Matt Vulich
#
#Creation Date: 2018-11-15
#
#############################

import psycopg2

#set database name
DBNAME = 'dbname=news'

#Find top 3 articles of all time
db = psycopg2.connect(DBNAME)
c = db.cursor()
c.execute("select a.title, count(l.id) as views from articles as a, log as l where (l.path like concat('%', a.slug) and l.status = '200 OK') group by a.title order by views desc limit 3")
articles = c.fetchall()
print("Top Articles of All Time:")
for row in articles:
    print " ", row[0], " - ", row[1], " Views"
db.close()

#Find Top authors of all time
db = psycopg2.connect(DBNAME)
c = db.cursor()
c.execute("select a.name, count(l.id) as views from authors as a, articles as art, log as l where art.author = a.id and l.path like concat('%', art.slug) and l.status = '200 OK' group by a.name order by views desc")
authors = c.fetchall()
print("Top Authors of All TIme")
for row in authors:
    print " ", row[0], " - ", row[1], " Views"
db.close()