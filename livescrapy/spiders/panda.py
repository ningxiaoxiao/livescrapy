
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from livescrapy.items import LivescrapyItem


class HuyaSpider(scrapy.Spider):
    name = 'panda'
    allowed_domains = ['panda.tv']
    start_urls = [
        'https://www.panda.tv/live_lists?status=2&order=person_num&token=&pagenum=120&pageno=1']

# https://www.panda.tv/live_lists?status=2&order=person_num&token=&pagenum=120&pageno=1

    def parse_room(self, res):

        j = json.loads(res.body)
        i = res.meta['item']

        i['fans'] = int(j['data']['fans'])
        yield i

    def parse(self, response):
        j = json.loads(response.body)

        for r in j['data']['items']:
            item = LivescrapyItem()
            item['platform'] = 'panda'

            item['online'] = int(r['person_num'])
            item['roomid'] = r['id']
            item['cate'] = r['classification']['cname']

            item['title'] = r['name']

            item['username'] = r['userinfo']['nickName']

            req = scrapy.Request(
                'https://www.panda.tv/room_followinfo?token=&roomid='+r['id'], self.parse_room)
            req.meta['item'] = item
            yield req

        # 从url中解出当前是第几页
        curpage = int(response.url.split('&')[-1].replace('pageno=', ''))
        # 从返回中得到总页数
        total = int(j['data']['total'])
        # 计算页数
        pgc = total/120+1
        if total % 120 == 0:
            pgc -= 1

        if curpage != pgc:
            curpage += 1
            yield response.follow('https://www.panda.tv/live_lists?status=2&order=person_num&token=&pagenum=120&pageno='+str(curpage), self.parse)
