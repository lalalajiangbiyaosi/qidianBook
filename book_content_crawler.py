import pymysql
import requests

db = pymysql.connect("106.14.168.122", "bingren11111", "li5266790", "biquge_book", use_unicode=True, charset="utf8")
cursor = db.cursor()
cursor.execute('select name,author from amazing_life_book')
result = cursor.fetchall()
baseUrl = ''
for i in result:
    (name,author) = i
    
