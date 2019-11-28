#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: config
@time: 2019/11/28:
"""
import random

base_url = 'http://www.e3ol.com/biography/inc_ajax.asp?types=index&a1=&a2=&a3=&a4=&a7=&a6=&a5=&key=&pageno={0}&callback=jQuery111307134604239631519_{1}&_={2}'
Token = [1574746246234, 1574754348161, 1574754403952]
t = random.choice(Token)
Request_Urls = [base_url.format(i, t, t + 1) for i in range(1,226)]