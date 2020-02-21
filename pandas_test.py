#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pandas
import os
import numpy
import logging
a=pandas.read_excel('medicine.xlsx',index_col=None,na_values=['NA'])
b=pandas.read_excel('medicinetwo.xlsx',index_col=None,na_values=['NA'])
a=a.rename(columns={"名字":'name','拼音名':'piny','别名':'other_name','来源':'laiyuan','性味':'xingwei','功能主治':'zhuzhi','用法用量':'yongfa','摘录':'zhailu'})
b=b.rename(columns={"名字":'name','拼音名':'piny','别名':'other_name','来源':'laiyuan','性味':'xingwei','功能主治':'zhuzhi','用法用量':'yongfa','摘录':'zhailu'})
a=a.replace('[]',numpy.nan)
a=a.dropna(how='any')
b=b.replace('[]',numpy.nan)
b=b.dropna(how='any')
c=a.append(b)
# print(a)
# print(b)
c=c.drop_duplicates()
# print(c)
title=['yaocai','laiyuan','xingwei','zhuzhi','yongfa','zhailu']
id_yaocai=[i for i in range(100000,112163)]
id_laiyuan=[i for i in range(200000,212163)]
id_xingwei=[i for i in range(300000,312163)]
id_zhuzhi=[i for i in range(400000,412163)]
id_yongfa=[i for i in range(500000,512163)]
id_zhailu=[i for i in range(600000,612163)]
# for i in id:
#     print(i)
c.index=range(len(c))
# print(c)
c['yaocai']=c['name']+c['piny']+c['other_name']
for i in title:
    d=c[i]
    e=pandas.DataFrame({i:d})
    if i=='yaocai':
        e.insert(0,'index:ID',id_yaocai)
    elif i=='laiyuan':
        e.insert(0,'index:ID',id_laiyuan)
    elif i=='xingwei':
        e.insert(0,'index:ID',id_xingwei)
    elif i=='zhuzhi':
        e.insert(0,'index:ID',id_zhuzhi)
    elif i=='yongfa':
        e.insert(0,'index:ID',id_yongfa)
    elif i=='zhailu':
        e.insert(0,'index:ID',id_zhailu)
    e.insert(2,':LABEL',[i for k in range(0,len(c))])
    # print(e)
    e.to_csv(i+".csv",index=False,encoding='utf_8_sig')
    print("写入成功")