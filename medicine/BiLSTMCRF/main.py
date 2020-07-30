# -*- coding:utf-8 -*-
# 功能描述：模型训练、测试的入口
import pickle
import sys
import yaml
import torch
import torch.optim as optim
from data_manager import DataManager
from model import BiLSTMCRF
from utils import f1_score, get_tags, format_result


class BiLSTMCRFEnter(object):

    def __init__(self, entry="train"):
        # 导入训练参数
        # 利用配置文件对main函数里面需要的变量进行初始化
        self.load_config()
        # 这里传入的entry是train，也就是训练集，也就是说对model初始化时是利用训练集对模型初始化的
        self.__init_model(entry)

    def __init_model(self, entry):
        # 模型训练的参数准备
        if entry == "train":
            #创建训练数据集的管理对象
            print(self.tags)
            self.train_manager = DataManager(batch_size=self.batch_size, tags=self.tags)
            print(self.train_manager.batch_data)
            print(len(self.train_manager.batch_data))
            self.total_size = len(self.train_manager.batch_data)
            # print(self.train_manager.batch_data)
            data = {
                "batch_size": self.train_manager.batch_size,
                "input_size": self.train_manager.input_size,
                "vocab": self.train_manager.vocab,
                "tag_map": self.train_manager.tag_map,
            }
            # 保存参数
            self.save_params(data)
            # 验证数据集的准备
            # 创建验证数据集的管理对象
            dev_manager = DataManager(batch_size=30, data_type="dev")
            # 通过data_manager中的迭代器不断将创建的数据管理器对象赋值到dev_batch中,用于下面计算损失的函数
            self.dev_batch = dev_manager.iteration()

            # 模型的主体使用的是BiLSTM来进行语义编码，CRF用来约束各个标签
            self.model = BiLSTMCRF(
                tag_map=self.train_manager.tag_map,
                batch_size=self.batch_size,
                vocab_size=len(self.train_manager.vocab),
                dropout=self.dropout,
                embedding_dim=self.embedding_size,
                hidden_dim=self.hidden_size,
            )
            # 加载恢复模型参数
            self.restore_model()
        # 模型用来预测的参数准备
        elif entry == "predict":
            data_map = self.load_params()
            input_size = data_map.get("input_size")
            self.tag_map = data_map.get("tag_map")
            self.vocab = data_map.get("vocab")
            # 这里创建一个模型对象model
            self.model = BiLSTMCRF(
                tag_map=self.tag_map,
                vocab_size=input_size,
                embedding_dim=self.embedding_size,
                hidden_dim=self.hidden_size
            )
            self.restore_model()

    def load_config(self):
        try:
            fopen = open("models/config.yml")
            #读取yml文件
            config = yaml.load(fopen)
            fopen.close()
        except Exception as error:
            print("Load config failed, using default config {}".format(error))
            #这里是重写config.yml文件
            fopen = open("models/config.yml", "w")
            config = {
                # 用于重写的数据，即初始化数据
                "embedding_size": 100,
                "hidden_size": 128,
                "batch_size": 50,
                "dropout": 0.5,
                "model_path": "models/",
                #这里原来的tags写成了tasg了，需要改过来
                "tags": ["Medicinal_Name", "Medicinal_Other_Name", "Medicinal_Function", "Medicinal_Taste", "Medicinal_Use_Num"]
            }
            yaml.dump(config, fopen)
            fopen.close()
        #重写过后再读取，感觉有点多此一举，主要就是将tags写进了config文件
        # word_embedding的维度大小
        self.embedding_size = config.get("embedding_size")
        # 隐藏层的维度
        self.hidden_size = config.get("hidden_size")
        # 每一个batch导入多少条数据
        self.batch_size = config.get("batch_size")
        # 模型的保存数据
        self.model_path = config.get("model_path")
        self.tags = config.get("tags")
        # 模型中神经百分之多少激活
        self.dropout = config.get("dropout")
        # 模型一共训练多少轮
        self.epoch = config.get("epoch")

    # 模型在测试过程中进行参数导入
    def restore_model(self):
        try:
            # 加载模型字典、
            # 这个load_state_dict函数并没有出现在任何一个文件中，所以这是怎么调用的？
            self.model.load_state_dict(torch.load(self.model_path + "params.pkl"))
            print("model restore success!")
        except Exception as error:
            print("model restore faild! {}".format(error))

    # 训练过程中保存模型的参数
    def save_params(self, data):
        with open("models/data.pkl", "wb") as fopen:
            pickle.dump(data, fopen)
    # 训练过程中读取更新后的模型的参数
    def load_params(self):
        # pkl文件的读取
        with open("models/data.pkl", "rb") as fopen:
            data_map = pickle.load(fopen)
            # print("*"*50+data_map+"*"*50)
        return data_map

    def train(self):
        # 使用Adam优化器进行梯度下降算法的优化迭代
        # 这里的parameters函数也没有在任何文件中声明过
        optimizer = optim.Adam(self.model.parameters(), lr=0.05)
        # optimizer = optim.SGD(ner_model.parameters(), lr=0.01)
        # 模型一共训练多少轮轮
        for epoch in range(self.epoch):
            index = 0
            # 获取每一个batch的数据
            for batch in self.train_manager.get_batch():
                index += 1
                self.model.zero_grad()

                sentences, tags, length = zip(*batch)
                sentences_tensor = torch.tensor(sentences, dtype=torch.long)
                tags_tensor = torch.tensor(tags, dtype=torch.long)
                length_tensor = torch.tensor(length, dtype=torch.long)

                # 计算模型训练过程中的损失

                loss = self.model.neg_log_likelihood(sentences_tensor, tags_tensor, length_tensor)
                # 进度加载
                progress = ("█" * int(index * 25 / self.total_size)).ljust(25)
                print("""epoch [{}] |{}| {}/{}\n\tloss {:.2f}""".format(
                    epoch, progress, index, self.total_size, loss.cpu().tolist()[0]
                )
                )
                self.evaluate()
                print("-" * 50)
                # 梯度回传
                loss.backward()
                # 优化器优化

                optimizer.step()
                # 保存模型
                torch.save(self.model.state_dict(), self.model_path + 'params.pkl')
                # torch.save(self.model)

    # 训练过程中的损失计算
    def evaluate(self):
        sentences, labels, length = zip(*self.dev_batch.__next__())
        _, paths = self.model(sentences)
        print("\teval")
        for tag in self.tags:
            f1_score(labels, paths, tag, self.model.tag_map)

    # 模型训练好之后的预测
    def predict(self, input_str=""):
        if not input_str:
            input_str = input("请输入文本: ")
        input_vec = [self.vocab.get(i, 0) for i in input_str]
        # convert to tensor
        sentences = torch.tensor(input_vec).view(1, -1)
        _, paths = self.model(sentences)
        entities = []
        for tag in self.tags:
            # 这里调用了工具类里面的get_tags用来对数据进行标注，就是标一些B-FUNC什么的
            tags = get_tags(paths[0], tag, self.tag_map)
            print(tag)
            print(self.tag_map)
            print(paths[0])
            print(tags)
            entities += format_result(tags, input_str, tag)

        return entities

        # 模型对文件中的句子进行实体预测
    def predict_file(self, f_r_path, f_w_path):
        # 去除重复预测的实体
        duplication = set()
        with open(f_r_path, encoding='utf-8') as f_r:
            with open(f_w_path, 'ab') as f_w:
                for line in f_r.readlines():
                    sent = line.split('\t')[-3].strip()
                    res = self.predict(sent)
                    for i in range(len(res)-1):
                        entity = res[i]['word']
                        tag=res[i]["type"]
                        if entity not in duplication:
                            # print(entity)
                            duplication.add(tag)
                            duplication.add(entity)
                            f_w.write((tag+" ： "+entity + '\n').encode())
                        if res[i]["type"]!=res[i+1]["type"]:
                            f_w.write('\n'.encode())
                        # f_w.write('\n'.encode())

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("menu:\n\ttrain\n\tpredict")
    #     exit()
    # if sys.argv[1] == "train":
    #     cn = BiLSTMCRFEnter("train")
    #     cn.train()
    # elif sys.argv[1] == "predict":
    #     cn = BiLSTMCRFEnter("predict")
    #     print(cn.predict())
    # 模型训练的入口
    cn = BiLSTMCRFEnter('train')
    cn.train()



    # 模型对文件中的句子进行实体预测
    # cn = BiLSTMCRFEnter("predict")
    # print(cn.predict(input()))

    # cn.predict_file('C:/Users/16016/PycharmProjects/medicine/medicine/BiLSTMCRF/data/medicine .txt', 'data/predict_entity.txt')
    # with open("models/data.pkl", "rb") as f:
    #     data_map = pickle.load(f)
    #     vocab = data_map.get("vocab", {})
    #     print(vocab)
    #     tag_map = data_map.get("tag_map", {})
    #     print(data_map)
    #     tags = data_map.keys()
    #     print(tags)

