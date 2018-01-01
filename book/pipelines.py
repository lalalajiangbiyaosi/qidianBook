# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from book.items import BiqugeItem,Book_content_Item
class BookPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,BiqugeItem):
            try:
                db = pymysql.connect("106.14.168.122", "bingren11111", "li5266790", "biquge_book", use_unicode=True, charset="utf8")
                cursor = db.cursor()
                print('replace into amazing_life_book(name,author,category,word_number,click_count,hot_share,brief,image_address) values(%s, %s, %s, %s, %s, %s, %s, %s)' %
                               (item['name'], item['author'], item['category'], item['word_number'],item['click_count'],item['hot_share'],item['brief'],item['image_add']))
                cursor.execute('replace into amazing_life_book(name,author,category,word_number,click_count,hot_share,brief,image_address) values(%s, %s, %s, %s, %s, %s, %s, %s)',
                               (item['name'], item['author'], item['category'], item['word_number'],item['click_count'],item['hot_share'],item['brief'],item['image_add']))
            except Exception as e :
                print("输出数据库错误----",e)
                with open('./err_book_index.txt', 'a', encoding='utf-8') as f:
                    f.write(item['id_name'] + '  ' + item['name'] + '  \n')
            finally:
                cursor.close()
                db.commit()
                db.close()
        else :
            db = pymysql.connect("106.14.168.122", "bingren11111", "li5266790", "biquge_book", use_unicode=True,
                                 charset="utf8")
            cursor = db.cursor()
            cursor.execute('select id from amazing_life_book where name = \'{}\''.format(item['book_name']))
            book_id = cursor.fetchall()[0][0]
            sqlLine = 'INSERT into amazing_life_chapter(chapter_name,chapter_id,book_id) values(\'%s\', %s, %s)' % (
            item['chapter_name'], item['chapter_id'], book_id,)
            try:
                cursor.execute(sqlLine)
            except Exception as e:
                print('书籍章节出输出数据库错误，错误原因为',e)
            finally:
                cursor.close()
                db.commit()
                db.close()
        return item
