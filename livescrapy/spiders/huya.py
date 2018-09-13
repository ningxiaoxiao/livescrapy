# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from livescrapy.items import LivescrapyItem

class HuyaSpider(scrapy.Spider):
    name = 'huya'
    allowed_domains = ['huya.com']
    start_urls = ['http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=0']
          
#http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page=0
#https://www.huya.com/kaerlol  
    def parse_room(self,res):

        room=res.selector.re("TT_ROOM_DATA = ([\\s\\S]*?);var")
        profile=res.selector.re("TT_PROFILE_INFO = ([\\s\\S]*?);var")
 
        roomjson=json.loads(room[0])
        profilejson=json.loads(profile[0])

        i=LivescrapyItem()
        i['platform']='huya'

        i['online']=int(roomjson['totalCount'])
        i['roomid']=roomjson['profileRoom']
        i['cate']=roomjson['gameFullName']

        i['title']=roomjson['introduction']

        i['username']=profilejson['nick']
        
        i['fans']=int(profilejson['fans'])
        yield i


    def parse(self, response):
        j=json.loads(response.body)
        for r in j['data']['datas']:
            
            yield scrapy.Request('https://www.huya.com/'+r['profileRoom'],self.parse_room)



        #从url中解出当前是第几页
        curpage=int(response.url.split('&')[-1].replace('page=',''))
        #从返回中得到总页数
        totalpage=int(j['data']['totalPage'])

        if curpage != totalpage:
            curpage+=1
            yield response.follow('http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page='+str(curpage),self.parse)


        
       
