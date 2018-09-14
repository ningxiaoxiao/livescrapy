
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from livescrapy.items import LivescrapyItem


class HuyaSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = [
        'https://api.live.bilibili.com/room/v1/room/get_user_recommend?page=1']

# https://api.live.bilibili.com/room/v1/room/get_user_recommend?page=1

    def parse_room(self, res):
        # 从中取出json信息
        
        baseinfo=res.selector.re(r'__NEPTUNE_IS_MY_WAIFU__=([\s\S]*?)</script>')

        if len(baseinfo) ==0:
            self.logger.warning('"%s" have no jsondata \r\n "%s"',res.url,res.body)

            return
       
        try:
            j = json.loads(baseinfo[0], encoding='utf-8')['baseInfoRes']['data']
            i = res.meta['item']

            i['fans'] = int(j['attention'])
            i['roomid'] = j['room_id']
            i['online'] = int(j['online'])
            i['title'] = j['title']
            i['cate'] = j['area_name']
            yield i
        except Exception as ex:
            self.logger.error(ex)
            self.logger.error(res)
            self.logger.error(baseinfo)
            self.logger.error(baseinfo[0])

    def parse(self, response):
        j = json.loads(response.body)

        for r in j['data']:
            item = LivescrapyItem()
            item['platform'] = 'bilibili'
            item['username'] = r['uname']
            req = scrapy.Request(
                'https://live.bilibili.com/'+str(r['roomid']), self.parse_room)
            req.meta['item'] = item
            yield req

        # 从url中解出当前是第几页
        curpage = int(response.url.split('?')[-1].replace('page=', ''))
        if len(j['data']) != 0:  # 已经得不到数据了
            curpage += 1
            yield response.follow('https://api.live.bilibili.com/room/v1/room/get_user_recommend?page='+str(curpage), self.parse)
