#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: CrawlPerson.py 
@time: 2019/11/26
"""

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Base_Url = 'http://www.e3ol.com/'
Chrome_Driver_Path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"

def init_driver():
    chrome_options = Options()
    # 接管已经打开的浏览器，需要在cmd中输入
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="F:\PythonDemo\MySpider\Damai\chrom_data"
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # prefs = {"profile.managed_default_content_settings.images":2}#不加载图片
    # chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(Chrome_Driver_Path, options=chrome_options)

    # 控制浏览器相应时间和界面大小
    driver.implicitly_wait(0.1)
    return driver


def main():
    url = 'http://www.e3ol.com/biography-index.html'
    # response = requests.get(url=url)
    driver = init_driver()
    driver.get(url=url)
    url_list = []
    while True:
        # html = bs(driver.page_source,'html.parser')
        # li_list = html.find('ul',attrs={'class':'about_list'})
        # l = li_list.find('li')
        # for li in li_list:
        #     li = li.find('div').find('a',href=True)
        #     url_list.append(li.get('href'))
        try:
            driver.find_element_by_xpath('//*[@id="page"]/a[4]').click()
        except Exception as e:
            print(e)
            break

    # print(url_list[0])
    # print(len(url_list))

if __name__ == '__main__':
    main()