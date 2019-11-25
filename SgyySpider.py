#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: SgyySpider
@time: 2019/11/25:
"""

import requests
import pickle
from bs4 import BeautifulSoup

def load_pkl():
    with open('data/sgyy.pkl','rb') as f:
        data = pickle.load(f)
    return data

def save_pkl(l):
    with open('data/sgyy.pkl','wb') as f:
        pickle.dump(l, f)
    print('save done!')

def parse_html(response):
    html = BeautifulSoup(response.text, 'html.parser')
    title = html.find_all('p')[1].find('font').find('b').get_text()
    content = html.find('pre').find('font').get_text()
    return title, content

def crawl_html(url):
    response = requests.get(url=url)
    response.encoding = 'GB2312'
    return parse_html(response)

def main():
    base_url = 'http://www.purepen.com/sgyy/{0}.htm'
    list_sgyy = []
    for i in range(1,121):
        dict_sgyy = {}
        i = str(i)
        print('爬取第{0}章'.format(i))
        if len(i) < 3 : i = '0'*(3-len(i)) + i
        url = base_url.format(i)
        title, content = crawl_html(url)
        dict_sgyy['chapter'] = i
        dict_sgyy['title'] = title.strip()
        dict_sgyy['content'] = content.strip()
        list_sgyy.append(dict_sgyy)
    save_pkl(list_sgyy)


if __name__ == '__main__':
    # main()
    data = load_pkl()
    print(data[10])

