# -*- coding:utf-8 -*-
# 功能描述：处理数据集为模型可读形式
import copy
import pickle as cPickle
import torch


# 处理数据的工具类
class DataManager():
    # 这里data_type默认是train，也就是说在main函数里面第一创建dataManager的对象时调用的是train的初始化方式
    def __init__(self, max_length=100, batch_size=20, data_type='train', tags=[]):
        self.index = 0
        self.input_size = 0
        self.batch_size = batch_size
        self.max_length = max_length
        self.data_type = data_type
        self.data = []
        self.batch_data = []
        self.vocab = {"unk": 0}
        # self.tag_map = {"O":0, "B-ORG":1, "I-ORG":2, "E-ORG":3, "B-PER":4, "I-PER":5, "E-PER":6, "S":7}
        self.tag_map = {'O': 0, 'START': 1, 'STOP': 2, 'B-Medicinal_Name': 3, 'E-Medicinal_Name': 4, 'B-Medicinal_Other_Name': 5, 'I-Medicinal_Other_Name': 6, 'E-Medicinal_Other_Name': 7, 'B-Medicinal_Function': 8, 'E-Medicinal_Function': 9, 'I-Medicinal_Function': 10, 'B-Medicinal_Use_Num': 11, 'I-Medicinal_Use_Num': 12, 'E-Medicinal_Use_Num': 13, 'B': 14, 'E': 15, 'I': 16, 'I-Medicinal_Name': 17, 'B-Medicinal_Taste': 18, 'E-Medicinal_Taste': 19, 'I-Medicinal_Taste': 20, 'S-Medicinal_Other_Name': 21, 'S-Medicinal_Taste': 22, 'S-Medicinal_Use_Num': 23, 'S-Medicinal_Function': 24}
        # 指定模型的功能{训练、验证、测试}
        if data_type == "train":
            assert tags, Exception("请指定需要训练的tag类型，如[\"ORG\", \"PER\"]")
            # 用于生成标签，并存储到data/train中
            self.generate_tags(tags)
            self.data_path = "data/train"
        elif data_type == "dev":
            self.data_path = "data/dev"
            # 加载标签用于验证是否
            self.load_data_map()
        elif data_type == "test":
            self.data_path = "data/test"
            self.load_data_map()

        self.load_data()
        self.prepare_batch()

    # 获取模型中需要用到的所有标签
    def generate_tags(self, tags):
        self.tags = []
        for tag in tags:
            for prefix in ["B-", "I-", "E-", "S-"]:
                self.tags.append(prefix + tag)
        self.tags.append("O")

    # 加载训练好的模型中的参数
    def load_data_map(self):
        with open("models/data.pkl", "rb") as f:
            self.data_map = cPickle.load(f)
            self.vocab = self.data_map.get("vocab", {})
            print(self.vocab)
            self.tag_map = self.data_map.get("tag_map", {})
            print(self.data_map)
            self.tags = self.data_map.keys()
            print(self.tags)

    # 将样本数据集处理成模型所需要的形式
    def load_data(self):
        # load data
        # add vocab
        # covert to one-hot
        sentence = []
        target = []
        with open(self.data_path, encoding='utf-8') as f:
            for line in f:
                # print(line)
                line = line[:-1]
                # print(line)
                # break
                # end为每一句话的结束符
                if line == "end":
                    self.data.append([sentence, target])
                    sentence = []
                    target = []
                    continue
                try:
                    word, tag = line.split(" ")
                except Exception:
                    continue
                if word not in self.vocab and self.data_type == "train":
                    self.vocab[word] = max(self.vocab.values()) + 1
                if tag not in self.tag_map and self.data_type == "train" and tag in self.tags:
                    self.tag_map[tag] = len(self.tag_map.keys())
                sentence.append(self.vocab.get(word, 0))
                target.append(self.tag_map.get(tag, 0))
        # 词表的大小
        self.input_size = len(self.vocab.values())
        print("{} data: {}".format(self.data_type, len(self.data)))
        print("vocab size: {}".format(self.input_size))
        print("unique tag: {}".format(len(self.tag_map.values())))
        print("-" * 50)
    #该函数好像并没有用到
    def convert_tag(self, data):
        # add E-XXX for tags
        # add O-XXX for tags
        _, tags = data
        converted_tags = []
        for _, tag in enumerate(tags[:-1]):
            if tag not in self.tag_map and self.data_type == "train":
                self.tag_map[tag] = len(self.tag_map.keys())
            converted_tags.append(self.tag_map.get(tag, 0))
        converted_tags.append(0)
        data[1] = converted_tags
        assert len(converted_tags) == len(tags), "convert error, the list dosen't match!"
        return data

    # 准备每一个batch样本数据集，即每次输入到模型中的一个batch数据集
    def prepare_batch(self):
        '''
            prepare data for batch
        '''
        index = 0
        while True:
            if index + self.batch_size >= len(self.data):
                # print("*" * 50)
                # print(self.data)
                pad_data = self.pad_data(self.data[-self.batch_size:])
                self.batch_data.append(pad_data)
                break
            else:
                pad_data = self.pad_data(self.data[index:index + self.batch_size])
                # print("*" * 50)
                # print(self.data)
                index += self.batch_size
                self.batch_data.append(pad_data)
    #该函数用于填充数据
    def pad_data(self, data):
        c_data = copy.deepcopy(data)
        max_length = max([len(i[0]) for i in c_data])
        for i in c_data:
            i.append(len(i[0]))
            i[0] = i[0] + (max_length - len(i[0])) * [0]
            i[1] = i[1] + (max_length - len(i[1])) * [0]
            # i[0] = torch.tensor(i[0])
            # i[1] = torch.tensor(i[1])
        return c_data

    def iteration(self):
        idx = 0
        while True:
            yield self.batch_data[idx]
            idx += 1
            if idx > len(self.batch_data) - 1:
                idx = 0

    def get_batch(self):
        for data in self.batch_data:
            yield data
