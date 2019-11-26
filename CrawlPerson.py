#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: CrawlPerson.py 
@time: 2019/11/26
"""
import re
import random
import requests
import pickle as pkl
import time

User_Agent = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)']

Token = [1574746246234,1574754348161,1574754403952]
url = 'http://www.e3ol.com/biography/inc_ajax.asp?types=index&a1=&a2=&a3=&a4=&a7=&a6=&a5=&key=&pageno={0}&callback=jQuery111307134604239631519_{1}&_={2}'

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
                else:
                    d[s[0]] = s[1][1:-1] #去掉首尾“”号
        except Exception as e:
            print(e)
            print(all_k_v)

        yield d

def save_data(l):
    with open('data/renwu.pkl','wb') as f:
        pkl.dump(l,f)
    print('save done!')

def crawl_page(page):
    res = []
    headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Referer': 'http://www.e3ol.com/biography-index.html',
        'User-Agent': random.choice(User_Agent),
        'X-Requested-With': 'XMLHttpRequest'
    }
    t = random.choice(Token)
    time.sleep(random.randint(0,3))

    response = requests.get(url=url.format(page, t, t + 1), headers=headers)
    response.encoding = 'ascii'
    for i in parse_response(response):
        if not isinstance(i, dict) or len(i) == 0: continue
        print('添加{0}'.format(i['name']))
        res.append(i)
    return res

def main():
    renwu_list = []
    for i in range(1,226):
        renwu_list.extend(crawl_page(i))
        print('完成{0}个'.format(len(renwu_list)))

    save_data(renwu_list)

if __name__ == '__main__':
    main()