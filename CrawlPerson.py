#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: CrawlPerson.py 
@time: 2019/11/26
"""

import os
import re
import random
import requests
import pickle as pkl
import time
import shutil
from urllib.request import urlopen
from bs4 import BeautifulSoup

User_Agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)']

Token = [1574746246234,1574754348161,1574754403952]
url = 'http://www.e3ol.com/biography/inc_ajax.asp?types=index&a1=&a2=&a3=&a4=&a7=&a6=&a5=&key=&pageno={0}&callback=jQuery111307134604239631519_{1}&_={2}'

def crawl_page(page):
    print('爬取页面{0}'.format(page))
    res = []
    headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Referer': 'http://www.e3ol.com/biography-index.html',
        'User-Agent': random.choice(User_Agent),
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'close',
    }
    t = random.choice(Token)
    time.sleep(random.randint(0,3))

    response = requests.get(url=url.format(page, t, t + 1), headers=headers)
    response.encoding = 'ascii'
    for i in parse_response(response):
        if not isinstance(i, dict) or len(i) == 0: continue
        retry_times = 0
        while not crawl_person(i):
            if retry_times > 3:
                break
            retry_times += 1
            print('重试次数{0}'.format(retry_times))
        print('添加{0}'.format(i['name']))
        res.append(i)
    return res

def parse_response(res):
    res = res.content.decode("unicode-escape")
    p1 = re.compile(r'[\[](.*)[\]]', re.S)  # 最小匹配
    soul = re.findall(p1, res)[0]
    p2 = re.compile(r'[{](.*?)[}]', re.S) # 最大匹配
    items = re.findall(p2, soul)
    for item in items:
        d = {}
        all_k_v = item.split(',')# bug 文本中可能含有,的逗号，而不是，逗号。
        try :
            for k_v in all_k_v:
                s = k_v.split(':')
                if s[0] == 'pic':
                    d[s[0]] = 'http://www.e3ol.com'+s[1][1:-1].replace('\\','')
                elif s[0] == 'id':
                    d[s[0]] = s[1] # id 不需要去除""
                elif s[0] == 'name_url':
                    d['url'] = 'http://www.e3ol.com/biography/html/{0}'.format(s[1][1:-1])
                elif s[0] == 'sex' or s[0] == 'name' or s[0] == 'zhengshi':
                    d[s[0]] = s[1][1:-1] #去掉首尾“”号

        except Exception as e:
            print(e)
            print(all_k_v)

        yield d


def parse_detail(d, response):
    bs = BeautifulSoup(response.text,'html.parser')
    name_list = bs.find('ul',attrs={'class':'name_list'}).find_all('li')
    name = name_list[0].get_text().split('\xa0')
    d['zi'] = name[len(name)-2]
    d['age'] = name[len(name)-1]
    jiguan = name_list[1].get_text().split('：')
    d['jiguan'] = jiguan[1]
    cata = name_list[2].get_text().split('\xa0')
    try:
        m_cata = cata[0]
        c_cata = []
        c_cata.append(cata[1].split('：')[1])
        c_cata.extend([x for x in cata[2:] if len(x)>0])
        d['cata'] = m_cata
        d['cata_list'] = c_cata
    except Exception as e:
        print(e)
        d['cata'] = cata[0]
        d['cata_list'] = cata
    d['guanzhi'] = [x for x in name_list[4].get_text().split('：')[1].split('\xa0') if len(x)>0]

    all_text = bs.find_all('div',attrs={'class':'text'})
    d['history'] = all_text[0].get_text().replace('\u3000\u3000','')

    try:
        all_text_span = all_text[1].find_all('span')
        d['chapter_list'] = [x.get('title') for x in all_text_span[0].find('div',attrs={'class':'ren_hui'}).find_all('li',attrs={'class':'a'})]
        d['total_chapter'] = all_text_span[0].find_all('tr')[0].find_all('td')[2].get_text()
        d['year_list'] = [x.get('title') for x in all_text_span[0].find('div',attrs={'class':'ren_year'}).find_all('li',attrs={'class':'a'})]
        d['total_year'] = all_text_span[0].find_all('tr')[1].find_all('td')[2].get_text()
        d['novel'] = all_text_span[1].get_text().replace('\u3000\u3000','')
    except Exception as e:
        print(e)
        d['chapter_list'] = []
        d['total_chapter'] = '0'
        d['year_list'] = []
        d['total_year'] = '0'
        d['novel'] = ''
    family = all_text[len(all_text)-2].find('ul').find_all('li')
    d['father'] = family[0].find_all('div')[1].get_text()
    d['mother'] = family[1].find_all('div')[1].get_text()
    d['mate'] = [x for x in family[2].find_all('div')[1].get_text().split('\xa0') if len(x)>0]
    d['child'] = [x for x in family[3].find_all('div')[1].get_text().split('\xa0') if len(x)>0]
    d['brother'] = [x for x in family[4].find_all('div')[1].get_text().split('\xa0') if len(x)>0]
    # return d

def crawl_person(person):
    # data = load_data()
    # for i in data:
    print('爬取人物{0}'.format(person['name']))
    time.sleep(1 + random.uniform(0, 2))
    headers = {
        'User-Agent': random.choice(User_Agent),
        'Referer': 'http://www.e3ol.com/biography-index.html',
        'Connection': 'close',
    }
    try :
        response = requests.get(url=person['url'],headers=headers)
    except Exception as e:
        print(e)
        return False

    response.encoding = 'utf-8'
    parse_detail(person,response)
    return True
def main():
    renwu_list = []
    for i in range(1,226):
        renwu_list.extend(crawl_page(i))
        print('完成{0}个'.format(len(renwu_list)))

    save_data(renwu_list)


def download_img(img_url,img_path):
    timeout_secs = 10
    # try retrieve the pdf
    if os.path.exists(img_path): return True
    try:
        print('fetching {0} into {1}'.format(img_url, img_path))
        req = urlopen(img_url, None, timeout_secs)
        with open(img_path, 'wb') as fp:
            shutil.copyfileobj(req, fp)
        time.sleep(1 + random.uniform(0, 2))
    except Exception as e:
        print('error downloading: {0}'.format(img_url))
        print(e)
        return False
    return True

def download_avatars():
    data = load_data()
    avatar_path = 'data/img/{0}'

    for i in data:
        retry_time = 0
        try :
            avatar_url = i['pic']
        except Exception as e:
            print(e)
            print(i)
            continue

        avatar_name = avatar_url.split('/')[-1]
        while True and retry_time < 3:
            if download_img(avatar_url, avatar_path.format(avatar_name)) : break
            else: retry_time += 1
    print('Save avatar done!')

def save_data(l):
    with open('data/renwu.pkl','wb') as f:
        pkl.dump(l,f)
    print('save done!')

def load_data():
    with open('data/renwu.pkl','rb') as f:
        data = pkl.load(f)
    return data


if __name__ == '__main__':
    main()
    # download_avatars()