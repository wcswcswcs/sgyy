#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: ToNeo4j
@time: 2019/12/9:
"""

import pandas as pd
from py2neo import Graph,Node,Relationship,Subgraph
graph = Graph("http://localhost:7474",auth=("neo4j","liuhaiyang210"))

# a = Node("Person", name="Alice")
# b = Node("Person", name="Bob")
# ab = Relationship(a, "KNOWS", b)
# graph.create(ab)
#

def add_renwu_nodes(data):
    renwu_list = data['实体1'].as_matrix()
    renwu_set = set([x.strip() for x in renwu_list if not x=='未知'])
    tx = graph.begin()
    nodes = []
    for name in renwu_set:
        oneNode = Node('Person',name=name)
        # 这里的循环，一般是把文件的数据存入node中
        nodes.append(oneNode)
    nodes = Subgraph(nodes)
    tx.create(nodes)
    tx.commit()

def add_shili_nodes(data):
    shili_list = []
    def process_relation_(value):
        if value['关系'] == 'cated' or value['关系'] == 'cata':
            shili_list.append(value['实体2'])
    data.apply(process_relation_,axis=1)
    shili_set = set(shili_list)
    tx = graph.begin()
    nodes = []
    for force in shili_set:
        oneNode = Node('Force',name=force)
        # 这里的循环，一般是把文件的数据存入node中
        nodes.append(oneNode)
    nodes = Subgraph(nodes)
    tx.create(nodes)
    tx.commit()

def add_relation(data):
    relations = []
    rel_map = {
        'mate':'配偶',
        'cata':'主效',
        'cated':'曾效力',
        'father':'父亲',
        'mother':'母亲',
        'brother':'兄弟'
    }
    tx = graph.begin()
    def process_relation_(value):
        name1 = value['实体1']
        name2 = value['实体2']
        relation = value['关系']
        if name2 == '未知':
            return
        if relation == 'cata' or relation == 'cated':
            b = graph.nodes.match("Force", name=name2).first()
        else:
            b = graph.nodes.match("Person", name=name2).first()
        a = graph.nodes.match("Person", name=name1).first()

        if a == None or b == None:
            return

        rel = Relationship(a, rel_map[relation], b)
        relations.append(rel)
    data.apply(process_relation_,axis=1)
    relations = Subgraph(relationships=relations)
    tx.create(relations)
    tx.commit()

if __name__ == '__main__':
    data_relation = pd.read_csv('data/renwu_relate.csv')
    add_renwu_nodes(data_relation)

    add_shili_nodes(data_relation)

    add_relation(data_relation)