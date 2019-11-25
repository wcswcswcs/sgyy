#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: jiagu_test
@time: 2019/11/25:
"""

import jiagu
from SgyySpider import load_pkl

if __name__ == '__main__':
    data = load_pkl()
    # d1 = data[2]
    text = '议温明董卓叱丁原　馈金珠李肃说吕布'
    print(jiagu.ner(text))