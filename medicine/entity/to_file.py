#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import pandas as pd
import csv

# 读取实体形成的，名称、关系、实体文件
h_r_t_name = [":START_ID", "role", ":END_ID"]
h_r_t = pd.read_table(r'C:\Users\taomin\Desktop\中药数据\entity_file.txt', decimal="\t", names=h_r_t_name)
print(h_r_t.info())
print(h_r_t.head())

# 去除重复实体
entity = set()
entity_h = h_r_t[':START_ID'].tolist()
entity_t = h_r_t[':END_ID'].tolist()
for i in entity_h:
    entity.add(i)
for i in entity_t:
    entity.add(i)
print(entity)
# 保存节点文件
csvf_entity = open(r'C:\Users\taomin\Desktop\中药数据\entity.csv', "w", newline='', encoding='utf-8')
w_entity = csv.writer(csvf_entity)
# 实体ID，要求唯一，名称，LABEL标签，可自己不同设定对应的标签
w_entity.writerow(("entity:ID", "name", ":LABEL"))
entity = list(entity)
entity_dict = {}
for i in range(len(entity)):
    w_entity.writerow(("e" + str(i), entity[i], "my_entity"))
    entity_dict[entity[i]] = "e"+str(i)
csvf_entity.close()
# 生成关系文件，起始实体ID，终点实体ID，要求与实体文件中ID对应，:TYPE即为关系
h_r_t[':START_ID'] = h_r_t[':START_ID'].map(entity_dict)
h_r_t[':END_ID'] = h_r_t[':END_ID'].map(entity_dict)
h_r_t[":TYPE"] = h_r_t['role']
h_r_t.pop('role')
h_r_t.to_csv(r'C:\Users\taomin\Desktop\中药数据\relation.csv', index=False)
