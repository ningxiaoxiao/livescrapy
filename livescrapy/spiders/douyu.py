# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from livescrapy.items import LivescrapyItem

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyu.com','douyucdn.cn']
    start_urls = ['https://www.douyu.com/gapi/rkc/directory/0_0/1']
    
#https://open.douyucdn.cn/api/RoomApi/room/156277
#https://www.douyu.com/gapi/rkc/directory/0_0/1
#https://www.douyu.com/directory/all
#得到分页数
    def parse_room(self,res):
        j=json.loads(res.body)
        j=j['data']
        i=LivescrapyItem()
        i['platform']='douyu'
        i['roomid']=j['room_id']
        i['cate']=j['cate_name']
        i['title']=j['room_name']
        i['username']=j['owner_name']
        i['online']=j['online']
        i['fans']=j['fans_num']
        yield i
       

    def parse(self, response):
        j=json.loads(response.body)
        for r in j['data']['rl']:
            #请求房间信息,
            yield scrapy.Request('https://open.douyucdn.cn/api/RoomApi/room/'+str(r['rid']),self.parse_room)
            

        #得到当前页
        urls=response.url.split('/')
        pgc=int(urls[-1])
        #得到总页数
       

        pgcnt=int(j['data']['pgcnt'])
        
        if pgc != pgcnt:
            pgc+=1
            yield response.follow('https://www.douyu.com/gapi/rkc/directory/0_0/'+str(pgc),self.parse)