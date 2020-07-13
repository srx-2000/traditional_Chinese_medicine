# coding:utf-8
import jieba
import xlrd
import numpy as np
import re
import string

#(Begin), I 表示内部(inside), O 表示外部(outside), E 表示这个词处于一个实体的结束为止， S 表示，这个词是自己就可以组成一个实体(Single)

def Creat_Txt():
 f=open('../资料/全部/jieba_data.txt','a+',encoding='utf-8')
 return f

def Add():
 print("添加字典进入jieba\n--------")
 # 将字典添加到jieba
 jieba.load_userdict('../资料/全部/jieba_data.txt')




def Open_Data(boolean):
 print("文件读入")
 print('------------------------')

 #打开文件
 Workbook = xlrd.open_workbook('../资料/全部/pandas_excel.xlsx')
 sheet = Workbook.sheet_by_index(0)

 #获取药材名称
 Medicinal_Name = sheet.col_values(1)
 #print(Medicinal_Name)

 #获取别名
 Medicinal_Other_Name=sheet.col_values(3)
 #print(Medicinal_Other_Name)

 # 获取来源
 Medicinal_From = sheet.col_values(4)
 #print(Medicinal_From)

 #获取性味
 Medicinal_Taste=sheet.col_values(5)
 #print(Medicinal_Taste)

 #获取功能
 Medicinal_Function=sheet.col_values(6)
 #print(Medicinal_Function)

 #获取用量
 Medicinal_Use_Num=sheet.col_values(7)
 #print(Medicinal_Use_Num)

 print('读入完成')
 print('---------------------')
 #展示数量是否相同
 print('数量展示\n')
 print('Medicinal_Name',len(Medicinal_Name))
 print('Medicinal_Use_Num',len(Medicinal_Use_Num))
 print('Medicinal_Function',len(Medicinal_Function))
 print('Medicinal_Taste',len(Medicinal_Taste))
 print('Medicinal_From',len(Medicinal_From))
 print('Medicinal_Other_Name',len(Medicinal_Other_Name),'\n-------------')

 #根据药材名进行去重
 Name=[]
 Num=[]
 for i in range(len(Medicinal_Name)):
  if Medicinal_Name[i] not in Name:
   Name.append(Medicinal_Name[i])
  else: Num.append(i)

 #for i in Num:
  #print(i)
  #print(Medicinal_Name[i])

 #后面数据都是重复的，所以需要删除 7373-12163
 del Medicinal_Name[7373:12163]
 del Medicinal_Use_Num[7373:12163]
 del Medicinal_Function[7373:12163]
 del Medicinal_Taste[7373:12163]
 del Medicinal_From[7373:12163]
 del Medicinal_Other_Name[7373:12163]

 #删除第一个
 del Medicinal_Name[0]
 del Medicinal_Use_Num[0]
 del Medicinal_Function[0]
 del Medicinal_Taste[0]
 del Medicinal_From[0]
 del Medicinal_Other_Name[0]

 print('去重后数量展示\n')
 print('Medicinal_Name',len(Medicinal_Name))
 print('Medicinal_Use_Num',len(Medicinal_Use_Num))
 print('Medicinal_Function',len(Medicinal_Function))
 print('Medicinal_Taste',len(Medicinal_Taste))
 print('Medicinal_From',len(Medicinal_From))
 print('Medicinal_Other_Name',len(Medicinal_Other_Name),'\n--------------------------')

 #对别名进行处理
 #将别名分开,括号是别名的来源，去除括号中的内容
 #展示顺序没变，先在这里输出一下

 #for i in Medicinal_Other_Name:
  #print(i)
 #print(Medicinal_Other_Name)
 Medicinal_Other_Name_1=[]
 for i in Medicinal_Other_Name:
  a=re.sub("\（.*?\）","",i)
  #print(a)
  Medicinal_Other_Name_1.append(a)
 #print(Medicinal_Other_Name_1)

 Medicinal_Other_Name=Medicinal_Other_Name_1

 #建立药名-别名,使用list作为值
 Medicinal_Other_Name_1=[]
 for i in Medicinal_Other_Name:
  a=list(re.split("、|，|。",i))
  #过滤空字符
  a=list(filter(None,a))
  #print(a)
  Medicinal_Other_Name_1.append(a)

 #print(len(Medicinal_Name))
 #print(Medicinal_Other_Name_1)
 Medicinal_Other_Name_2=[]
 #获取所有的别名，存的时候存这个
 for i in range(len(Medicinal_Other_Name_1)):
  for j in Medicinal_Other_Name_1[i]:
   if j not in Medicinal_Other_Name_2:
    Medicinal_Other_Name_2.append(j)

 Name2OtherName={}
 for i in range(len(Medicinal_Name)):
   key=Medicinal_Name[i]
   value=Medicinal_Other_Name_1[i]
   Name2OtherName.setdefault(key,value)

 #print(Name2OtherName)

 #药材来源目前不做标注
 #print(Medicinal_From)

 Medicinal_Taste_1=[]
 #这个是将所有的性味进行统计之后的，存入字典存入的是这个
 for i in Medicinal_Taste:
  a=re.sub("\《.*?\》",'',i)
  a=re.sub("[A-Za-z0-9\!\%\[\]\,\：\"\①]","",a)
  b=list(re.split("、|，|。|；",a))
  # 过滤空字符
  b = list(filter(None, b))
  for j in b:
   if j not in Medicinal_Taste_1:
    Medicinal_Taste_1.append(j)

 #print(len(Medicinal_Taste_1))

 Medicinal_Function_1=[]
 #功能
 for i in Medicinal_Function:
  a = re.sub("\《.*?\》", '', i)
  a = re.sub("[A-Za-z0-9\!\%\[\]\,\：\"\①\（\）\“\”]", "", a)
  b=list(re.split("、|，|。|；", a))
  # 过滤空字符
  b = list(filter(None, b))
  for j in b:
   if j not in Medicinal_Function_1:
    Medicinal_Function_1.append(j)

 #print(Medicinal_Function_1)
 #print(Medicinal_Use_Num)

 Medicinal_Use_Num_1=[]
 for i in Medicinal_Use_Num:
  a = re.sub("[A-Za-z0-9\!\%\[\]\,\"\①\（\）\“\”\～\-\.\钱\两]", "", i)
  b = list(re.split("：|，|。|；|:|;|、", a))
  # 过滤空字符
  b = list(filter(None, b))
  for j in b:
   if j not in Medicinal_Use_Num_1:
    Medicinal_Use_Num_1.append(j)
 #print(Medicinal_Use_Num_1)

 if boolean:
  print("开始建立字典\n-------------")
  # 创建自定义字典,也就是一个txt，里面每一行是词语、词频（可省略）、词性（可省略）
  f = Creat_Txt()
  for i in range(len(Medicinal_Name)):
   f.write(Medicinal_Name[i] +'\n')

  for i in range(len(Medicinal_Other_Name_2)):
   f.write(Medicinal_Other_Name_2[i]+"\n")

  for i in range(len(Medicinal_Taste_1)):
   f.write(Medicinal_Taste_1[i] +"\n")

  for i in range(len(Medicinal_Function_1)):
   f.write(Medicinal_Function_1[i] + "\n")

  for i in range(len(Medicinal_Use_Num_1)):
   f.write(Medicinal_Use_Num_1[i] +"\n")
  f.close()
  print("建立完成\n----------")
  boolean=False

 Add()


 print("拼接语料\n-----------")
 Str=[]
 w=0
 for i in range(len(Medicinal_Name)):
  w=w+1
  print(w,'/',len(Medicinal_Name))
  str=""
  str=str+Medicinal_Name[i]+" "
  str=str+Medicinal_Other_Name[i]+" "
  str=str+Medicinal_Function[i]+" "
  str=str+Medicinal_Taste[i]+" "
  str=str+Medicinal_Use_Num[i]+" "
  str=str+Medicinal_From[i]+" "
  Str.append(str)
 #print(str)
 print('拼接完成')
 return Str,Medicinal_Name,Medicinal_Other_Name_2,Medicinal_From,Medicinal_Function_1,Medicinal_Use_Num_1,Medicinal_Taste_1


def Numo(num):
 str=''
 for i in range(len(num)):
  if i==0:
   str=str+num[i]+" B-jiliang\n"
  elif i==len(num):
   str=str+num[i]+" E-jiliang\n"
  else:
   str=str+num[i]+" I-jiliang\n"

 return str


def Chinese(Str,name):
 a=''
 if len(Str)==1:
  a=Str+' S-'+name+'\n'
 else:
    for w in range(len(Str)):
     if w==0:
      a=a+Str[w]+' B-'+name+'\n'
     elif w==len(Str)-1:
      a=a+Str[w]+' E-'+name+'\n'
     else:
      a=a+Str[w]+' I-'+name+'\n'
 return a

def Cut():
 str,Medicinal_Name,Medicinal_Other_Name,Medicinal_From,Medicinal_Function,Medicinal_Use_Num,Medicinal_Taste=Open_Data(False)
 #str="我是谁"
 str=['金银花，中药名。为忍冬科忍冬属植物忍冬Lonicera japonica Thunb.、华南忍冬Lonicera confusa （Sweet） DC.、菰腺忍冬Lonicera hypoglauca Miq.、黄褐毛忍冬Lonicera fulvotomentosa Hsu et S. C. Cheng的花蕾。植物忍冬多分布于华东、中南、西南及河北、山西、辽宁、陕西、甘肃等地；华南忍冬多分布于广东、广西、海南；菰腺忍冬分布于浙江、安徽、福建、江西、湖北、湖南、广东、广西、四川、贵州、云南、台湾等；黄褐毛忍冬分布于广西、贵州、云南。具有清热解毒之功效。主治外感风热或温病发热，中暑，热毒血痢，痈肿疔疮，喉痹，多种感染性疾病。']
 print('获取完成')
 Output=[]
 #判断是否是中文
 bo = re.compile(u'[\u4e00-\u9fa5]')
 #判断是否是标点符号
 punc=['、','，','：','。',' ']
 #数字的处理，遇到非数字时将其输出
 Isnum=False
 Num=''
 Isstr=False
 Str=''
 First=True
 q=0
 for i in str:
  q=q+1
  print(q,'/',7373)
  a=(jieba.lcut(i))
  for j in a:
   d=bo.search(j)
   #不是中文
   if not d :
    #是标点符号
    if j in punc:
     if Isnum:
      p=Numo(Num)
      Num=''
      Isnum=False
      Output.append(p)

     Output.append(j+'\n')
     #不是标点符号，就是英文或者数字
     #是数字
    elif j.isdigit():
      Num=Num+j
      Isnum=True

    else:
     if Isnum:
      p = Numo(Num)
      Num = ''
      Isnum = False
      Output.append(p)

     Str=Str+'\n'+j
     Isstr=True


 #中文处理
   else:
    if Isnum:
     p = Numo(Num)
     Num = ''
     Isnum = False
     Output.append(p)
    if First:
     if j in Medicinal_Name:
      p=Chinese(j,'Medicinal_Name')
      Output.append(p)
      First=False
    elif j in Medicinal_Use_Num:
     p=Chinese(j,'Medicinal_Use_Num')
     Output.append(p)
    elif j in Medicinal_Function:
     p = Chinese(j, 'Medicinal_Function')
     Output.append(p)
    elif j in Medicinal_Taste:
     p = Chinese(j, 'Medicinal_Taste')
     Output.append(p)
    elif j in Medicinal_From:
      p = Chinese(j, 'Medicinal_From')
      Output.append(p)
    elif j in Medicinal_Other_Name:
     p = Chinese(j, 'Medicinal_Other_Name')
     Output.append(p)
    else:
     if len(j)==1:
      p=j+' S\n'
      Output.append(p)
     else:
      p=''
      for w in range(len(j)):
       if w==0:
        p=p+j[w]+' B\n'
       elif w==len(j)-1:
        p=p+j[w]+' E\n'
       else:
        p=p+j[w]+' I\n'
      Output.append(p)
 print('进行写入')
 f = open('../资料/全部/Data.txt', 'a+', encoding='utf-8')
 for z in Output:
  f.write(z)
 print('写入完成')





Cut()

