# -*- coding:utf-8 -*-
# 工具函数

# 规范输出结果的函数
# 将输入的list【stop和start】和text结合，生成出相对应的词汇
def format_result(result, text, tag):
    entities = []
    for i in result:
        begin, end = i
        entities.append({
            "start":begin,
            "stop":end + 1,
            "word":text[begin:end+1],
            "type":tag
        })
    return entities

# 这里的输入以一条最佳的词向量路径
# 第二个参数tag应该是FUNC
# 第三个参数为tag_map={'O': 0, 'START': 1, 'STOP': 2, 'B-FUNC': 3, 'E-FUNC': 4, 'I-FUNC': 5}
def get_tags(path, tag, tag_map):
    # 此下五行代码是用来生成的相应的tag标签的即：B-FUNC等等
    # 这里在生成B-FUNC之后，会利用B-FUNC找到其对应的数字，在我们这里我们可以根据上面给出的tag_map，找出B-FUNC对应的是：3
    begin_tag = tag_map.get("B-" + tag)
    mid_tag = tag_map.get("I-" + tag)
    end_tag = tag_map.get("E-" + tag)
    single_tag = tag_map.get("S")  # 这里的S-FUNC好像并没有与之对应的tag_map元素
    o_tag = tag_map.get("O")
    # 这里将begin赋值为一个负数，是一个不可能达到的值（最低为0）
    begin = -1
    end = 0
    tags = []
    last_tag = 0
    for index, tag in enumerate(path): # 这里是枚举出来路径上每一个词向量上的数，以及这个数所对应的位置的索引用index来存储，比如：[3,4,0,3,4,0,3,5,4,0,0],那么根据上面分析得到此时的词向量可以化为[B-FUNC,E-FUNC,O,B-FUNC,E -FUNC.......................]
        # 这里是说如果tag=3（对应的就是B-FUNC）并且索引为0，那么就将begin赋值为0，下面的与这个类似
        if tag == begin_tag and index == 0:
            begin = 0
        elif tag == begin_tag:
            begin = index
        elif tag == end_tag and last_tag in [mid_tag, begin_tag] and begin > -1:
            end = index
            tags.append([begin, end])
        elif tag == o_tag or tag == single_tag:
            begin = -1
        last_tag = tag
    return tags

def f1_score(tar_path, pre_path, tag, tag_map):
    origin = 0.
    found = 0.
    right = 0.
    for fetch in zip(tar_path, pre_path):
        tar, pre = fetch
        tar_tags = get_tags(tar, tag, tag_map)
        pre_tags = get_tags(pre, tag, tag_map)

        origin += len(tar_tags)
        found += len(pre_tags)

        for p_tag in pre_tags:
            if p_tag in tar_tags:
                right += 1

    recall = 0. if origin == 0 else (right / origin)
    precision = 0. if found == 0 else (right / found)
    f1 = 0. if recall+precision == 0 else (2*precision*recall)/(precision + recall)
    print("\t{}\trecall {:.2f}\tprecision {:.2f}\tf1 {:.2f}".format(tag, recall, precision, f1))
    return recall, precision, f1