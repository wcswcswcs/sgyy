# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SgyyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    zi = scrapy.Field()
    age = scrapy.Field()
    zhengshi = scrapy.Field()
    jiguan = scrapy.Field()
    father = scrapy.Field()
    mother = scrapy.Field()
    brother = scrapy.Field()
    mate = scrapy.Field()
    child = scrapy.Field()
    guanzhi = scrapy.Field()
    cata = scrapy.Field()
    cata_list = scrapy.Field()
    total_year = scrapy.Field()
    year_list = scrapy.Field()
    total_chapter = scrapy.Field()
    chapter_list = scrapy.Field()
    history = scrapy.Field()
    novel = scrapy.Field()
    pic = scrapy.Field()
    url = scrapy.Field()

    def from_dict(self, d):
        for k in d.keys():
            self[k] = d[k]

    def to_dict(self):
        d = {}
        for k in self.keys():
            d[k] = self[k]
        return d

    def to_list(self):
        res = []
        colums = ['id','name','sex','zi','age','zhengshi','jiguan',
                       'father','mother','brother','mate','child','guanzhi','cata','cata_list',
                       'total_year','year_list','total_chapter','chapter_list','history','novel','pic','url']
        for k in colums:
            res.append(self[k])

        return res

