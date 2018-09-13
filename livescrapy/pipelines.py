# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import datetime

class MysqlPipeline(object):
    def __init__(self):
        self.connect=pymysql.connect(
            host='192.168.1.55',#yj ubantu
            port=3306,
            db='scrapy',
            user='root',
            passwd='123456',
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor=self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            "insert into \
            %s\
            (timestamp,platform,title,username,online,fans,cate,rid)\
            value\
            ('%s','%s','%s','%s','%d','%d','%s','%s')"%\
            (item['platform'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),item['platform'],item['title'],item['username'],item['online'],int(item['fans']),item['cate'],item['roomid'])
        )

        self.connect.commit()
        
        return item
