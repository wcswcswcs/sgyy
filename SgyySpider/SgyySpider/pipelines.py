# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pickle as pkl
import pandas as pd
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

def save_data(l):
    with open('../../data/renwu.pkl','wb') as f:
        pkl.dump(l,f)
    print('save done!')

class SgyyspiderPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.datas = []
    def process_item(self, item, spider):
        print('添加{0}到pickl'.format(item['name']))
        self.datas.append(item.to_dict())
        return item

    def spider_closed(self, spider):
        if self.datas != None and len(self.datas) > 0:
            save_data(self.datas)

        print('Save data len {0}'.format(len(self.datas)))


class ToCsvPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.colums = ['编号','名字','性别','字号','年龄','正史','籍贯',
                       '父亲','母亲','兄弟','配偶','孩子','官职','主效','效力',
                       '总年数','年代列表','总章节','章节列表','历史','小说','头像','链接']
        self.datas = []

    def process_item(self, item, spider):
        print('添加{0}到csv'.format(item['name']))
        self.datas.append(item.to_list())
        return item

    def spider_closed(self, spider):
        if self.datas != None and len(self.datas) > 0:
            new_data = pd.DataFrame(self.datas)
            new_data.to_csv('../../data/renwu.csv', header=self.colums, index=False)
        print('Save data len {0}'.format(len(self.datas)))