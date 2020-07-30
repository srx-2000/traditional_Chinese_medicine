# -*- coding:utf-8 -*-
# 功能描述：使用BiLSTMCRF进行语义编码、维特比算法进行解码
import copy

import numpy as np

import torch
import torch.nn.functional as F
from torch import nn

START_TAG = "START"
STOP_TAG = "STOP"


# view用法：https://zhuanlan.zhihu.com/p/87856193?from_voters_page=true


# 计算整个损失函数loss的辅助函数
# 好像是用来帮助做矩阵加法用的
# 应该是用来计算发射矩阵和转移矩阵的和用的
def log_sum_exp(vec):
    max_score = torch.max(vec, 0)[0].unsqueeze(0)
    max_score_broadcast = max_score.expand(vec.size(1), vec.size(1))
    result = max_score + torch.log(torch.sum(torch.exp(vec - max_score_broadcast), 0)).unsqueeze(0)
    return result.squeeze(1)


class BiLSTMCRF(nn.Module):

    # 模型参数的初始化过程
    # 这里dim指的都是维度
    # 具体的概念层的东西可以到以下地址补一下：
    # https://www.cnblogs.com/pinard/p/6945257.html（像什么隐藏层之类的这里面都有举例，但具体的这个代码好像用的不是这个模型，所以只要知道一些基本概念就好了）
    # https://www.zhihu.com/question/20136144（这里面的第二个回答举得生病的例子可以用来练练手，下面的维特比算法也有提到这个链接）
    def __init__(
            self,
            tag_map={'O': 0, 'START': 1, 'STOP': 2, 'B-Medicinal_Name': 3, 'E-Medicinal_Name': 4, 'B-Medicinal_Other_Name': 5, 'I-Medicinal_Other_Name': 6, 'E-Medicinal_Other_Name': 7, 'B-Medicinal_Function': 8, 'E-Medicinal_Function': 9, 'I-Medicinal_Function': 10, 'B-Medicinal_Use_Num': 11, 'I-Medicinal_Use_Num': 12, 'E-Medicinal_Use_Num': 13, 'B': 14, 'E': 15, 'I': 16, 'I-Medicinal_Name': 17, 'B-Medicinal_Taste': 18, 'E-Medicinal_Taste': 19, 'I-Medicinal_Taste': 20, 'S-Medicinal_Other_Name': 21, 'S-Medicinal_Taste': 22, 'S-Medicinal_Use_Num': 23, 'S-Medicinal_Function': 24},
            #据目前查到的资料来看，这个batch_size是一次处理的橘子的个数
            batch_size=20,
            vocab_size=20,
            # 这里的隐藏层就我目前的理解，应该是：内置属性，咱们看不见的东西
            # 举个例子：就用上面链接中的，三个盒子抽白球红球，其中每个盒子中白红球数量不一样
            # 那么可观测层就应该是白球和红球
            # 由于每个盒子中球的数目不等，所以会有很多不等的概率，但每个盒子中的概率相加为1，而这个就成为可观测矩阵
            # 而隐藏层就是盒子1，盒子2，盒子3。
            # 同时这个隐藏层也有很多内规则，比如：如果当前抽球的盒子是第一个盒子，则以0.5的概率仍然留在第一个盒子继续抽球，以0.2的概率去第二个盒子抽球，以0.3的概率去第三个盒子抽球。如果当前抽球的盒子是第二个盒子，则以0.5的概率仍然留在第二个盒子继续抽球，以0.3的概率去第一个盒子抽球，以0.2的概率去第三个盒子抽球。...........
            # 这也就使其也会生成一个3*3的矩阵，这个矩阵我们就叫状态转移分布矩阵（以上都是对HHM模型来说的）
            # 然后我们要预测的数据输出出来的应该是抽三次之后的球的颜色都是什么比如为：{红，白，红}，这个叫做观测序列
            # 最后一个就是我们需要给他一个初始状态分布，用来初始化第一次抽取球的时候从哪个箱子开始抽，准确来说就是一个概率序列如：{0.2，0.4，0.4}
            # 这个初始化状态分布的作用是用来初始化隐藏层的，在初始化之后隐藏层就可以自己不断地执行下去了。（以上是对上面链接中的红白球的例子的个人理解）
            hidden_dim=128,
            dropout=0.5,
            embedding_dim=100
    ):
        super(BiLSTMCRF, self).__init__()
        self.batch_size = batch_size
        self.hidden_dim = hidden_dim
        self.embedding_dim = embedding_dim
        self.vocab_size = vocab_size
        self.dropout = dropout

        self.tag_size = len(tag_map)
        self.tag_map = tag_map

        '''这里应该是随机初始化一个tag_size*tag_size大小的矩阵，用以作为状态转移矩阵
        并将该矩阵绑定到Module中，以便后面可以对初始化的这个转移矩阵进行参数优化'''
        self.transitions = nn.Parameter(
            torch.randn(self.tag_size, self.tag_size)
        )
        '''这里的.data是从原来绑定到transitions上的parameter中以tensor的形式取出那个随机矩阵，并根据上面的全局变量进行截取'''
        '''self.transitions.data[:, self.tag_map[START_TAG]] = -1000.的操作的意思是：
        通过self.tag_map（一个字典）中的START标签定位到其的value是1，那么式子就变为了self.transitions.data[:, 1] = -1000.
        而这里data[:,1]是numpy中截取二维数组中一维数据的方法，所以上面那个式子的意思就变为了，截取self.transitions这个二维数组的第1维的所有数据并将其赋值为-1000.
        而self.transitions.data[self.tag_map[STOP_TAG], :] = -1000.同理，只不过在字典中对应下来的STOP标签的value是2，那就截取第二维的所有数据并赋值为-1000.'''
        self.transitions.data[:, self.tag_map[START_TAG]] = -1000.
        self.transitions.data[self.tag_map[STOP_TAG], :] = -1000.

        '''https://blog.csdn.net/qq_31829611/article/details/90263794'''
        self.word_embeddings = nn.Embedding(vocab_size, self.embedding_dim)

        #这个函数好像涉及到关键了
        #目前有用的资料有
        # https://zhuanlan.zhihu.com/p/41261640（这个一定要看，注释非常详细）
        # https://blog.csdn.net/yangyang_yangqi/article/details/84585998（这个主要看那个图）
        # 就本实验来讲，由于我们做的是文章中的实体识别，所以这里第一个参数为句子长度，第二个参数为多少个句子，第三个参数为这个句子中选出的单词的维度数（这个维度数主要用来存放各种的词向量，毕竟一个词可以用到不同的语义中，在每个语义中都会有一个词向量与它对应，就可以想象成一个点，有好多箭头从这个点里面指出来，指出来的每个方向都是一个意思）（但好像这个代码里面并没有第三个参数，而文章中有说要严格遵循三维张量，所以并不是很懂这里）
        # num_layers：lstm隐层的层数，默认为1
        # bidirectional：True则为双向lstm默认为False
        # batch_first：True则输入输出的数据格式为 (batch, seq, feature)
        # dropout：除最后一层，每一层的输出都进行dropout，默认为: 0（这里代码设成了1，应该就算是启动了）
        # 这里还要提一句一般的LSTM都是单向的，但是BiLSTM是双向的，具体可以看第二个链接中的那个视图，和下面的例子，
        # 整体来说就是一句话分为好多个词，然后正着过去每个词（不是字）都创建一个词向量，然后反过来，再每个词都创建一个词向量，将二者拼起来形成一个词向量就是BiLSTM
        # 然后通过形成的词向量与后输入的词进行对比，算出应该的词（以上都是个人理解，具体直接看上面两个链接即可）
        '''先看这里！！！这里之所以有两个参数，是因为此时的神经层的详细结构还没确定，而下面的函数表达的意思是
        输入单词用一个维度为embedding_dim的向量表示, 隐藏层的一个维度hidden_dim // 2，仅有一层的神经元，
        仅仅是说这个网络可以接受[seq_len,batch_size,3]的数据输入，
        
        
        这里之所以用embedding_dim来创建，是因为此时的套接字的每个
        维度都用来存储一个词向量，所以等于给一个词创建了一个100平米的大房子，每平米都住着一个他的孩子
        '''
        self.lstm = nn.LSTM(self.embedding_dim, self.hidden_dim // 2,
                            num_layers=1, bidirectional=True, batch_first=True, dropout=self.dropout)
        self.hidden2tag = nn.Linear(self.hidden_dim, self.tag_size)
        self.hidden = self.init_hidden()

    # 隐藏层的初始化
    # 返回两个随机初始化的张量，其中的每个元素都是小于一的
    def init_hidden(self):
        return (torch.randn(2, self.batch_size, self.hidden_dim // 2),
                torch.randn(2, self.batch_size, self.hidden_dim // 2))

    # 使用lstm捕获语义特征
    '''# 即调用上面的定义好的 self.lstm 以获取lstm层的输出'''
    def __get_lstm_features(self, sentence):
        # 初始化hidden层
        self.hidden = self.init_hidden()
        # sentence.shape[1]是返回该矩阵的第一维的长度
        length = sentence.shape[1]
        '''这里传入的句子应该是一个tensor,然后根据这个句子的tensor，利用上面建好的embeddings，给每个句子tensor中的元素加载对应的映射，映射的维度应该是self.embedding_dim
        然后在利用view方法对或得到的embeddings重构为一个self.batch_size*length*self.embedding_dim大小的张量
        其中对于embedding处理的资料为：https://blog.csdn.net/qq_31829611/article/details/90263794'''
        embeddings = self.word_embeddings(sentence).view(self.batch_size, length, self.embedding_dim)
        # 这里的lstm_out是用来获取所有的隐状态值, 而用 "hidden" 的值来
        # 进行序列的反向传播运算, 具体方式就是将它作为参数传入后面的 LSTM 网络.
        # 这里我也不太懂，猜测是用来返回隐藏层的某些信息吧，因为好像隐藏层是交给神经网络去做的，所以要返回隐藏层的信息以用来后面的处理吧
        '''下面三步加起来的作用是：将构建好的lstm模型拿来进行运算，然后取出lstm_out（输出），并对lstm_out 进行重构，取最后一个时刻的输出。
        lstm_out的格式是（batch，time step，input），所以下面的view()中的-1就是取time step的最后一个，然后再放进hidden2tag（即nn.Linear（输出层）)
        得到logits（即为bilstm层的输出）'''
        lstm_out, self.hidden = self.lstm(embeddings, self.hidden)
        lstm_out = lstm_out.view(self.batch_size, -1, self.hidden_dim)
        # 这里猜测是，用返回过来的lstm_out，来控制hidden2tag，并将控制完后的张量返回给logits(这里说的控制，就类似于给一张二维的矩阵，利用返回来的类似开关的lstm_out，控制，哪里应该是1，哪里应该是0，但是具体隐藏层返回回来的控制信息能将这个二维张量中的数据怎么改变并不知道)
        # 这里由上面创建hidden2tag时我们可以知道，hidden2tag其实是一个列（或者行）数为hidden_size的，行（或者列）数为tag_size的二维矩阵（这样就可以控制，一个词的属性了，比如：中国这个词，tag_map就可以表示为{0,1,0,1,1,1}）
        logits = self.hidden2tag(lstm_out)
        return logits


    '''在这以后的四个方法，都为用于计算loss的方法'''
    def real_path_score_(self, feats, tags):
        # Gives the score of a provided tag sequence
        score = torch.zeros(1)
        tags = torch.cat([torch.tensor([self.tag_map[START_TAG]], dtype=torch.long), tags])
        for i, feat in enumerate(feats):
            score = score + self.transitions[tags[i], tags[i + 1]] + feat[tags[i + 1]]
        score = score + self.transitions[tags[-1], self.tag_map[STOP_TAG]]
        return score

    #计算
    def real_path_score(self, logits, label):
        '''
        caculate real path score
        :params logits -> [len_sent * tag_size]
        :params label  -> [1 * len_sent]

        Score = Emission_Score + Transition_Score
        Emission_Score = logits(0, label[START]) + logits(1, label[1]) + ... + logits(n, label[STOP])
        Transition_Score = Trans(label[START], label[1]) + Trans(label[1], label[2]) + ... + Trans(label[n-1], label[STOP])
        '''
        #创建一个全为0的矢量
        score = torch.zeros(1)
        #创建一个以tag_map列表为元素的矢量，并将其中的元素与label进行拼接
        label = torch.cat([torch.tensor([self.tag_map[START_TAG]], dtype=torch.long), label])
        #遍历传入的词向量表
        for index, logit in enumerate(logits):
            emission_score = logit[label[index + 1]]
            transition_score = self.transitions[label[index], label[index + 1]]
            score += emission_score + transition_score
        #计算分数
        score += self.transitions[label[-1], self.tag_map[STOP_TAG]]
        return score

    # 计算整个句子预测的得分
    def total_score(self, logits, label):
        """
        caculate total score

        :params logits -> [len_sent * tag_size]
        :params label  -> [1 * tag_size]

        SCORE = log(e^S1 + e^S2 + ... + e^SN)
        """
        obs = []
        #这里是创建一个1*6的张量，里面全是0
        previous = torch.full((1, self.tag_size), 0)

        for index in range(len(logits)):
            # 将原来1*6的张量扩展为6*6的张量
            previous = previous.expand(self.tag_size, self.tag_size).t()
            #将原来的词向量扩展为6*6的张量
            obs = logits[index].view(1, -1).expand(self.tag_size, self.tag_size)
            #好像是矩阵的加法
            scores = previous + obs + self.transitions
            previous = log_sum_exp(scores)
        #然后一直加到tag=STOP位置
        previous = previous + self.transitions[:, self.tag_map[STOP_TAG]]
        # caculate total_scores
        total_scores = log_sum_exp(previous.t())[0]
        return total_scores

    # 计算log损失
    def neg_log_likelihood(self, sentences, tags, length):
        #这里的batch_size是一次性处理的句子的个数，而sentences.size(0)则是传入的sentences张量的第0维的大小
        self.batch_size = sentences.size(0)
        #这里的调用与下面的forward里面一样，这里就不赘述了
        logits = self.__get_lstm_features(sentences)
        #建立一个全为0的向量
        real_path_score = torch.zeros(1)
        #建立一个全为0的向量
        total_score = torch.zeros(1)
        for logit, tag, leng in zip(logits, tags, length):
            #这里好像整个项目都没有用到整个函数，所以我也不太清楚他穿进来的tags是个啥.....并不是很能理解为啥tag还要截断一下
            logit = logit[:leng]
            tag = tag[:leng]
            #这里调用了上面的函数real_path_score
            real_path_score += self.real_path_score(logit, tag)
            #这里调用了上面的函数total_score
            total_score += self.total_score(logit, tag)
        # print("total score ", total_score)
        # print("real score ", real_path_score)
        #返回两者的差，即损失
        return total_score - real_path_score

    # 神经网络前向传播，抽取每个句子中的特征

    def forward(self, sentences, lengths=None):
        """
        翻译:这里的参数sentence是用来被预测的句子，这里传入的句子应该是一个tensor
        :params sentences sentences to predict
        翻译：参数lengths是句子的真实长度，默认值为-1
        :params lengths represent the ture length of sentence, the default is sentences.size(-1) #默认句子大小为-1
        """
        #个人猜测这里是使用传进来的句子组成了一个矩阵

        sentences = torch.tensor(sentences, dtype=torch.long)
        sen_size=sentences.size()
        #如果没有长度，那么将传进的句子的长度默认设为-1
        if not lengths:
            lengths = [i.size(-1) for i in sentences]
        #这里将批处理数量设置为句子大小
        self.batch_size = sentences.size(0)
        # 调用函数抽取特征
        #这里提取完了之后，应该就是一个充满词向量的二维表（词向量就类似于上面举得那个例子：tag_map就可以表示为{0,1,0,1,1,1}，只不过隐藏层控制的行（或列）可能还包含更多信息，以方便进一步区分词和词）
        logits = self.__get_lstm_features(sentences)
        #得分和路径初始化
        scores = []
        paths = []
        #该zip函数用于将参数中的迭代器打包成组，并将组形成list
        for logit, leng in zip(logits, lengths):
            #我猜测这个是用来根据长度截取词的，比如：吃饭饭，如果传入的长度为2，则截取到吃饭，如果传入的参数为3，则是吃饭饭
            logit = logit[:leng]
            #这里调用维特比解码，并接受返回的得分和路径（可以想象一个矩阵，然后按列与分别算他们的得分，并求出全局最大或最小的得分的路径）
            score, path = self.__viterbi_decode(logit)
            #更新上述初始化后的数组
            scores.append(score)
            paths.append(path)
        return scores, paths


    # 维特比算法具体的解释在：https://www.zhihu.com/question/20136144 链接中有很简单和详细的解释，我就不在这里瞎逼逼了
    # 假设有很多列，有点像贪心，每次找出局部最优解，然后删除其他解，然后再往后推进一列，最后到最终的点，再根据前面的给出的一系列局部最优解，找出全局最优解
    # 使用维特比算法进行解码
    # 这个解码过程是算法上的....我就不太会了，不过原理在上面链接里面
    def __viterbi_decode(self, logits):
        #个人猜测是回溯点数组，用于存储回头回溯时返回的最佳路径
        backpointers = []
        #创建一个全是0的矩阵（张量）
        trellis = torch.zeros(logits.size())
        #和上面一样，只不过变成长整型的了
        backpointers = torch.zeros(logits.size(), dtype=torch.long)

        trellis[0] = logits[0]
        for t in range(1, len(logits)):
            v = trellis[t - 1].unsqueeze(1).expand_as(self.transitions) + self.transitions
            trellis[t] = logits[t] + torch.max(v, 0)[0]
            backpointers[t] = torch.max(v, 0)[1]
        viterbi = [torch.max(trellis[-1], -1)[1].cpu().tolist()]
        backpointers = backpointers.numpy()
        for bp in reversed(backpointers[1:]):
            viterbi.append(bp[viterbi[-1]])
        viterbi.reverse()

        viterbi_score = torch.max(trellis[-1], 0)[0].cpu().tolist()
        return viterbi_score, viterbi
    # 获取状态转移矩阵
    def get_tran(self):
        return self.transitions
    # 功能与上述代码类似，解码过程
    def __viterbi_decode_v1(self, logits):
        init_prob = 1.0
        trans_prob = self.transitions.t()
        prev_prob = init_prob
        path = []
        for index, logit in enumerate(logits):
            if index == 0:
                obs_prob = logit * prev_prob
                prev_prob = obs_prob
                prev_score, max_path = torch.max(prev_prob, -1)
                path.append(max_path.cpu().tolist())
                continue
            obs_prob = (prev_prob * trans_prob).t() * logit
            max_prob, _ = torch.max(obs_prob, 1)
            _, final_max_index = torch.max(max_prob, -1)
            prev_prob = obs_prob[final_max_index]
            prev_score, max_path = torch.max(prev_prob, -1)
            path.append(max_path.cpu().tolist())
        return prev_score.cpu().tolist(), path
