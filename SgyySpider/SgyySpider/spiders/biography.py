# -*- coding: utf-8 -*-

import re
import time
import random
import scrapy
from bs4 import BeautifulSoup
from ..items import SgyyspiderItem
from ..config import Request_Urls
from ..settings import User_Agent

class BiographySpider(scrapy.Spider):
    name = 'biography'
    allowed_domains = ['www.e3ol.com']
    start_urls = Request_Urls
    index = 0
    split = '|'

    def parse(self, response):
        for i in self.parse_response(response.body):
            if not isinstance(i, dict) or len(i) < 3: continue # 过滤掉名字中带{}，导致正则解析出错的人物 http://www.e3ol.com/biography/html/%E8%A7%A3%7B%E5%BF%84%E5%89%BD%7D/
            self.index += 1
            print('{0}爬取人物{1}'.format(self.index, i['name']))
            time.sleep(1 + random.uniform(0, 2))
            headers = {
                'User-Agent': random.choice(User_Agent),
                'Referer': 'http://www.e3ol.com/biography-index.html',
            }
            yield scrapy.Request(url=i['url'],
                                 meta={'id': i['id'], 'url': i['url'], 'sex': i['sex'],
                                       'pic': i['pic'], 'zhengshi': i['zhengshi'], 'name': i['name']},
                                 headers=headers, callback=self.parse_detail)

    def parse_response(self, res):
        res = res.decode("unicode-escape")
        p1 = re.compile(r'[\[](.*)[\]]', re.S)  # 最小匹配
        soul = re.findall(p1, res)[0]
        p2 = re.compile(r'[{](.*?)[}]', re.S)  # 最大匹配
        items = re.findall(p2, soul)
        for item in items:
            d = {}
            all_k_v = item.split(',')  # bug 文本中可能含有,的逗号，而不是，逗号。
            try:
                for k_v in all_k_v:
                    s = k_v.split(':')
                    if s[0] == 'pic':
                        d[s[0]] = 'http://www.e3ol.com' + s[1][1:-1].replace('\\', '')
                    elif s[0] == 'id':
                        d[s[0]] = s[1]  # id 不需要去除""
                    elif s[0] == 'name_url':
                        d['url'] = 'http://www.e3ol.com/biography/html/{0}'.format(s[1][1:-1])
                    elif s[0] == 'sex' or s[0] == 'name' or s[0] == 'zhengshi':
                        d[s[0]] = s[1][1:-1]  # 去掉首尾“”号

            except Exception as e:
                print(e)
                print(all_k_v)

            yield d

    def parse_detail(self, response):
        d = SgyyspiderItem()
        d['id'] = response.meta['id']
        d['url'] = response.meta['url']
        d['sex'] = response.meta['sex']
        d['pic'] = response.meta['pic']
        d['zhengshi'] = response.meta['zhengshi']
        d['name'] = response.meta['name']
        bs = BeautifulSoup(response.text, 'html.parser')
        name_list = bs.find('ul', attrs={'class': 'name_list'}).find_all('li')
        name = name_list[0].get_text().split('\xa0')
        d['zi'] = name[len(name) - 2]
        d['age'] = name[len(name) - 1]
        jiguan = name_list[1].get_text().split('：')
        d['jiguan'] = jiguan[1]
        cata = name_list[2].get_text().split('\xa0')
        try:
            m_cata = cata[0]
            c_cata = []
            c_cata.append(cata[1].split('：')[1])
            c_cata.extend([x for x in cata[2:] if len(x) > 0])
            d['cata'] = m_cata
            d['cata_list'] = self.split.join(c_cata)
        except Exception as e:
            print(e)
            d['cata'] = cata[0]
            d['cata_list'] = self.split.join(cata)
        d['guanzhi'] = self.split.join([x for x in name_list[4].get_text().split('：')[1].split('\xa0') if len(x) > 0])

        all_text = bs.find_all('div', attrs={'class': 'text'})
        d['history'] = all_text[0].get_text().replace('\u3000\u3000', '')

        try:
            all_text_span = all_text[1].find_all('span')
            d['chapter_list'] = self.split.join([x.get('title') for x in
                                 all_text_span[0].find('div', attrs={'class': 'ren_hui'}).find_all('li', attrs={
                                     'class': 'a'})])
            d['total_chapter'] = all_text_span[0].find_all('tr')[0].find_all('td')[2].get_text()
            d['year_list'] = self.split.join([x.get('title') for x in
                              all_text_span[0].find('div', attrs={'class': 'ren_year'}).find_all('li',
                                                                                                 attrs={'class': 'a'})])
            d['total_year'] = all_text_span[0].find_all('tr')[1].find_all('td')[2].get_text()
            d['novel'] = all_text_span[1].get_text().replace('\u3000\u3000', '')
        except Exception as e:
            print(e)
            d['chapter_list'] = '未知'
            d['total_chapter'] = '0'
            d['year_list'] = '未知'
            d['total_year'] = '0'
            d['novel'] = '未知'
        family = all_text[len(all_text) - 2].find('ul').find_all('li')
        d['father'] = family[0].find_all('div')[1].get_text()
        d['mother'] = family[1].find_all('div')[1].get_text()
        d['mate'] = self.split.join([x for x in family[2].find_all('div')[1].get_text().split('\xa0') if len(x) > 0])
        d['child'] = self.split.join([x for x in family[3].find_all('div')[1].get_text().split('\xa0') if len(x) > 0])
        d['brother'] = self.split.join([x for x in family[4].find_all('div')[1].get_text().split('\xa0') if len(x) > 0])
        yield d