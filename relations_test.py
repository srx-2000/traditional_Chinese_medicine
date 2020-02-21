#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pandas as pd
import numpy

id_yaocai=[i for i in range(100000,112163)]
id_laiyuan=[i for i in range(200000,212163)]
id_xingwei=[i for i in range(300000,312163)]
id_zhuzhi=[i for i in range(400000,412163)]
id_yongfa=[i for i in range(500000,512163)]
id_zhailu=[i for i in range(600000,612163)]

yaocai_laiyuan=pd.DataFrame({":START_ID":id_laiyuan,":END_ID":id_yaocai,'relation':["belong" for i in range(len(id_yaocai))],':TYPE':["belong" for i in range(len(id_yaocai))]})
# print(yaocai_laiyuan)
yaocai_xingwei=pd.DataFrame({":START_ID":id_xingwei,":END_ID":id_yaocai,'relation':["belong" for i in range(len(id_yaocai))],':TYPE':["belong" for i in range(len(id_yaocai))]})
yaocai_zhuzhi=pd.DataFrame({":START_ID":id_yaocai,":END_ID":id_zhuzhi,'relation':["effect" for i in range(len(id_yaocai))],':TYPE':["effect" for i in range(len(id_yaocai))]})
yaocai_yongfa=pd.DataFrame({":START_ID":id_yaocai,":END_ID":id_yongfa,'relation':["method" for i in range(len(id_yaocai))],':TYPE':["method" for i in range(len(id_yaocai))]})
yaocai_zhailu=pd.DataFrame({":START_ID":id_yaocai,":END_ID":id_zhailu,'relation':["from" for i in range(len(id_yaocai))],':TYPE':["from" for i in range(len(id_yaocai))]})


yaocai_laiyuan.to_csv('yaocai_laiyuan.csv',index=False,encoding='utf_8_sig')
yaocai_xingwei.to_csv('yaocai_xingwei.csv',index=False,encoding='utf_8_sig')
yaocai_zhuzhi.to_csv('yaocai_zhuzhi.csv',index=False,encoding='utf_8_sig')
yaocai_yongfa.to_csv('yaocai_yongfa.csv',index=False,encoding='utf_8_sig')
yaocai_zhailu.to_csv('yaocai_zhailu.csv',index=False,encoding='utf_8_sig')
print("写入成功")