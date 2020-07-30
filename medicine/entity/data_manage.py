import pandas as pd
import re

# 合并数据集
def merge_data():
    data1 = pd.read_csv(r'C:\Users\taomin\Desktop\中药数据\medicineone.csv')
    data2 = pd.read_csv(r'C:\Users\taomin\Desktop\中药数据\medicinetwo.csv')

    # 去并集
    data_merge = pd.merge(data1, data2, on=['名字', '拼音名', '别名', '来源', '性味', '功能主治', '用法用量', '摘录'], how='outer')

    # 按照名字去重
    data_merge = data_merge.drop_duplicates(subset=['名字'])
    data_merge.to_csv(r'C:\Users\taomin\Desktop\中药数据\medicine.csv')
    print(data_merge.info())


# 将csv文件转换为txt
def csv_to_txt():
    data = pd.read_csv(r'C:\Users\taomin\Desktop\中药数据\medicine.csv', encoding='utf-8')
    with open(r'C:\Users\taomin\Desktop\中药数据\medicine.txt', 'a+', encoding='utf-8') as f:
        for line in data.values:
            f.write((str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\t' + str(line[3]) + '\t' +
                     str(line[4]) + '\t' + str(line[5]) + '\t' + str(line[6]) + '\t' + str(line[7]) + '\t' +
                     str(line[8]) + '\n'))


# 得到实体
def get_entity():
    # 去重字典
    duplication = dict()
    #
    with open(r'C:\Users\taomin\Desktop\中药数据\medicine.txt', encoding='utf-8') as f_r:
        for line in f_r.readlines():
            # 药品名字
            name = line.split('\t')[1].strip()
            name = get_NULL(name)

            # 拼音名
            pinyin_name = line.split('\t')[2].strip()
            pinyin_name = get_NULL(pinyin_name)

            # 别名
            otherName_sent = line.split('\t')[3]
            otherNames = re.split("""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·和及]""", otherName_sent)
            otherNames = [other_name.strip() for other_name in otherNames if other_name and "《" not in other_name
                          and "》" not in other_name and other_name != 'nan']
            otherName_entity_sent = '，'.join(otherNames)
            otherName_entity_sent = get_NULL(otherName_entity_sent)
            # print(otherName_entity_sent)

            # 来源
            source_sent = line.split('\t')[4].strip()
            sources = \
                source_sent.split('来源于')[-1].split('来源')[-1].split('。')[0].split('：')[-1].split('为')[-1].split('，')[0]
            sources_entity_sent = sources
            sources_entity_sent = get_NULL(sources_entity_sent)
            # print(sources_entity_sent)

            # 性味
            flavor_sent = line.split('\t')[5].strip()
            flavors = re.split("""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·和及]""", flavor_sent)
            flavors = [flavor.strip() for flavor in flavors if flavor and "《" not in flavor and "》" not in flavor and flavor != 'nan']
            flavor_entity_sent = '，'.join(flavors)
            flavor_entity_sent = get_NULL(flavor_entity_sent)
            # print(flavor_entity_sent)

            # 功能主治
            functions_sent = line.split('\t')[-3].replace('《', '').replace('》', '').replace('①', '') \
                .replace('用于', '').replace('主治', '').replace('主', '').replace('等症', '')

            functions = re.split("""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·和及]""", functions_sent)
            functions = [entity for entity in functions if entity]
            function_entity_sent = '，'.join(functions)
            function_entity_sent = get_NULL(function_entity_sent)
            # print(function_entity_sent)

            # 用法用量
            usage = line.split('\t')[-2].strip()
            usage = get_NULL(usage)

            # 摘录
            extract_sent = line.split('\t')[-1].strip()
            extracts = re.split("""[《》]""", extract_sent)
            extracts = [extract.strip() for extract in extracts if extract]
            extract_entity_sent = '，'.join(extracts)
            extract_entity_sent = get_NULL(extract_entity_sent)
            # print(extract_entity_sent)


            # 将实体提取到get_entity.txt文件中
            with open(r'C:\Users\taomin\Desktop\中药数据\get_entity.txt', 'ab') as f_w1:
                f_w1.write((name + '\t' + pinyin_name + '\t' + otherName_entity_sent + '\t' +
                            sources_entity_sent + '\t' + flavor_entity_sent + '\t' + function_entity_sent + '\t' +
                            usage + '\t' + extract_entity_sent + '\n').encode('utf-8'))


def get_NULL(variable):
    if not variable or variable == '[]' or variable == 'nan':
        return 'NULL'
    else:
        return variable

#形成实体文件 名称、关系、实体模式
def entity_file():
    with open(r'C:\Users\taomin\Desktop\中药数据\get_entity.txt', encoding='utf-8') as f_r:
        with open(r'C:\Users\taomin\Desktop\中药数据\entity_file.txt', 'ab') as f_w:
            for line in f_r.readlines():
                name, pinyin_name, otherName_entity_sent, sources_entity_sent, flavor_entity_sent,\
                function_entity_sent, usage, extract_entity_sent = line.split('\t')

                help_to_entity_file(name, pinyin_name, '拼音名', f_w)
                help_to_entity_file(name, otherName_entity_sent, '别名', f_w)
                help_to_entity_file(name, sources_entity_sent, '来源', f_w)
                help_to_entity_file(name, flavor_entity_sent, '性味', f_w)
                help_to_entity_file(name, function_entity_sent, '功能主治', f_w)
                help_to_entity_file(name, usage, '用法用量', f_w)
                help_to_entity_file(name, extract_entity_sent.strip(), '摘录', f_w)

#名称、关系、实体模式
def help_to_entity_file(name, entity_sent, relation, f_w):
    if entity_sent != 'NULL':
        if '，' not in entity_sent or relation == '用法用量':
            triple = name + '\t' + relation + '\t' + entity_sent + '\n'
            f_w.write(triple.encode())
        else:
            entity_list = entity_sent.split('，')
            for entity in entity_list:
                triple = name + '\t' + relation + '\t' + entity + '\n'
                f_w.write(triple.encode())

entity_file()