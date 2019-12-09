#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: GeneralRelation
@time: 2019/12/9:
"""
import pandas as pd

if __name__ == '__main__':
    rela_list = []

    df = pd.read_csv('data/renwu_process_v1.csv')
    def mate_rela(value):
        name = value['名字']
        mates = value['配偶'].split("|")
        for mate in mates:
            rela_list.append([value['编号'], name, 'mate', mate])


    def cata_rela(value):
        name = value['名字']
        cateds = value['效力'].split("|")
        for cata in cateds:
            if cata == value['主效']:
                rela_list.append([value['编号'], name, 'cata', cata])
            else:
                rela_list.append([value['编号'], name, 'cated', cata])


    def brother_rela(value):
        name = value['名字']
        brothers = value['兄弟'].split("|")
        for brother in brothers:
            rela_list.append([value['编号'], name, 'brother', brother])


    def father_rela(value):
        name = value['名字']
        father = value['父亲']
        rela_list.append([value['编号'], name, 'father', father])


    def mother_rela(value):
        name = value['名字']
        mother = value['母亲']
        rela_list.append([value['编号'], name, 'mother', mother])


    df.apply(mate_rela, axis=1)
    df.apply(cata_rela, axis=1)
    df.apply(brother_rela, axis=1)
    df.apply(father_rela, axis=1)
    df.apply(mother_rela, axis=1)

    rela_colume = ['编号', '实体1', '关系', '实体2']

    rela_df = pd.DataFrame(columns=rela_colume, data=rela_list)
    rela_df.to_csv('data/renwu_relate.csv', index=False)