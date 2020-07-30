# 实体消歧
import synonyms

# 使用synonyms近义词包，通过设定阈值来进行实体消歧
def get_synonyms_word(word):
    # 查找与实体相近的词
    ret_tuple = synonyms.nearby(word)
    word_list = synonyms.nearby(word)[0]
    score_list = synonyms.nearby(word)[1]
    # 设定阈值，查找与所输入的实体相近的实体
    for x, y in zip(word_list, score_list):
        if y > 0.6 and y < 1:
            #print(x)
            yield x


def get_entity():
    # 去重实体集合
    duplication = set()

    # 获取medicine_entity.txt文件中所有的功能主治实体
    with open(r'C:\Users\taomin\Desktop\中药数据\get_entity.txt', encoding='utf-8') as f_r:
    # with open('test', encoding='utf-8') as f_r:
        for line in f_r.readlines():
            function_entity_list = line.split('\t')[-3].split('，')
            for entity in function_entity_list:
                duplication.add(entity)
            # function_entity_list = line.strip()
            # duplication.add(function_entity_list)
    # 所有实体集合的拷贝
    dup_copy = duplication.copy()

    # 将相近的实体进行去重
    for entity in duplication:
        print('正在处理', entity)
        for synonyms_entity in get_synonyms_word(entity):
            if synonyms_entity in dup_copy:
                print('移除%s' % (synonyms_entity))
                dup_copy.remove(synonyms_entity)

    # 将去除了相近的实体集合进行保存
    print(dup_copy)
    with open(r'C:\Users\taomin\Desktop\中药数据\function_entity_disambiguation.txt', 'ab') as f_w2:
        for entity in dup_copy:
            f_w2.write((entity+'\n').encode())

get_entity()