import pymysql
import hashlib
from config import MYSQLCONFIG
from flask import Markup
import markdown

def mark(con):
  contents = Markup(markdown.markdown(con))
  return contents

conn = pymysql.connect(
	host = MYSQLCONFIG['host'],
	port = MYSQLCONFIG['port'],
	user = MYSQLCONFIG['user'],
	passwd = MYSQLCONFIG['password'],
	db = MYSQLCONFIG['db'],
	charset = MYSQLCONFIG['charset'])

cursor = conn.cursor()

def courseAdd(name, teacher, dsp, bgdate, eddate):
	cursor.execute("insert into course(name, teacher, dsp, bgdate, eddate, rddate) values(%s, %s, %s, %s, %s, now())", (name, teacher, dsp, bgdate, eddate))
	conn.commit()

courseAdd('database', 'yh', 'this is an interesting introductino to database', '2017-11-26 08:30:00', '2017-11-286 16:30:00')
