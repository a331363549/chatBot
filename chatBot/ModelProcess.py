__author__ = 'ding'
'''
pyspark 贝叶斯模型的处理
'''
import numpy as np
from pyhanlp import *
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vector, Vectors
from scipy.sparse import csr_matrix
from .Bayes import NaiveBayesModel
import jieba.posseg as pseg
import jieba
from pypinyin import pinyin, lazy_pinyin


class ModelProcess:
    def __init__(self):
        self.abstractDict = dict()
        self.modelIndex = 0
        self.questionsPattern = self.loadQuestionsPattern()
        self.vocabulary = self.loadVocabulary()
        self.nbModel = self.loadClassifierModel()

    def analyQuery(self, querySentence):
        querySentence = querySentence.strip().lstrip()
        print("原始句子：" + querySentence)
        print("========HanLP分词开始========")

        # 抽象句子，对关键词进行抽象
        abstr = self.queryAbstract(querySentence)
        print('句子抽象化结果：' + abstr)

        # 将抽象的句子与训练集模板匹配，拿到对应模板
        strPatt = self.queryClassify(abstr)
        print('句子套用模板结果：' + strPatt)

        finalPattern = self.queryExtenstion(strPatt)
        print("原始句子替换成系统可识别的结果：" + finalPattern)
        return finalPattern

    # 问句抽象化
    def queryAbstract(self, querySentence):
        # terms = HanLP.segment(querySentence)
        terms = pseg.cut(querySentence)
        abstractQuery = ''
        nrCount = 0
        # for term in terms:
        jieba.load_userdict('./dish.txt')
        for word, cx in terms:
            # word = term.word
            # cx = term.nature.name
            print(word, cx)
            if cx == 'nz':
                abstractQuery += 'nz '
                self.abstractDict['nz'] = word
            elif cx == "nr" and nrCount == 0:
                abstractQuery += "nnt "
                self.abstractDict["nnt"] = word
                nrCount += 1
            elif cx == 'nr' and nrCount == 1:
                abstractQuery += "nnr "
                self.abstractDict["nnr"] = word
                nrCount += 1
            elif cx == 'x':
                abstractQuery += "x "
                self.abstractDict["x"] = word
            elif cx == 'ng':
                abstractQuery += "ng "
                self.abstractDict["ng"] = word
            else:
                abstractQuery += word + " "
        print("========HanLP分词结束========")
        return abstractQuery

    # 模板还原成句子
    def queryExtenstion(self, queryPattern):
        keys = self.abstractDict.keys()
        for key in keys:
            if key in queryPattern:
                value = self.abstractDict[key]
                queryPattern = queryPattern.replace(key, value)
            else:
                queryPattern = '没有匹配到正确的模板'
        extendedQuery = queryPattern
        # 当前句子处理完成，抽象dict释放空间，等待下一个句子的处理
        self.abstractDict.clear()
        # self.abstractDict = None
        return extendedQuery

    # 加载词汇表
    def loadVocabulary(self):
        vocabulary = dict()
        with open('./chatBot/question/vocabulary.txt', 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                vocabulary[line.split(':')[0]] = line.split(':')[1].replace('\n', '')
            return vocabulary

    # 加载文件返回内容
    def loadFile(self, filename):
        content = ''
        with open(filename, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                content += line + '`'
        return content

    # 句子分词后与词汇表记性key匹配转换为向量数组
    def sentenceToVector(self, sentence):
        vector = np.zeros(len(self.vocabulary))
        segment = HanLP.segment(sentence)
        for word in segment:
            word = word.word
            try:
                key = int(self.get_key(self.vocabulary, word)[0])
                vector[key] = 1
            except:
                continue
        return vector

    # 根据value返回字典中的key
    def get_key(self, dic, value):
        return [k for k, v in dic.items() if v == value]

    # 加载贝叶斯模型
    def loadClassifierModel(self):
        train_list = list()

        # 0,评分
        scoreQuestions = self.loadFile("./chatBot/question/【0】评分.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToVector(sentence)
            train_one = LabeledPoint('0.0', Vectors.dense(array))
            train_list.append(train_one)

        # 1,类型
        scoreQuestions = self.loadFile("./chatBot/question/【1】类型.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToVector(sentence)
            train_one = LabeledPoint('1.0', Vectors.dense(array))
            train_list.append(train_one)

        # 2,信息
        scoreQuestions = self.loadFile("./chatBot/question/【2】菜品信息.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToVector(sentence)
            train_one = LabeledPoint('2.0', Vectors.dense(array))
            train_list.append(train_one)

        # 3,价格
        scoreQuestions = self.loadFile("./chatBot/question/【3】菜的价格.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToVector(sentence)
            train_one = LabeledPoint('3.0', Vectors.dense(array))
            train_list.append(train_one)

        # 4,加入点餐列表
        scoreQuestions = self.loadFile("./chatBot/question/【4】加入菜单.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToVector(sentence)
            train_one = LabeledPoint('4.0', Vectors.dense(array))
            train_list.append(train_one)

        # 5,移除菜单
        scoreQuestions = self.loadFile("./chatBot/question/【5】移除菜单.txt")
        sentences = scoreQuestions.split("`")
        for sentence in sentences:
            array = self.sentenceToVector(sentence)
            train_one = LabeledPoint('5.0', Vectors.dense(array))
            train_list.append(train_one)

        conf = SparkConf().setAppName('NaiveBayesTest').setMaster('local[*]')
        sc = SparkContext(conf=conf)
        distData = sc.parallelize(train_list, numSlices=10)
        nb_model = NaiveBayes.train(distData)
        return nb_model

    # 加载问题模板
    def loadQuestionsPattern(self):
        questionsPattern = dict()
        with open('./chatBot/question/question_classification.txt', 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                questionsPattern[line.split(':')[0]] = line.split(':')[1].replace('\n', '')
        return questionsPattern

    # 贝叶斯分类器的结果，拿到匹配的分类标签，返回问题模板
    def queryClassify(self, sentence):
        array = self.sentenceToVector(sentence)
        v = Vectors.dense(array)
        index = self.nbModel.predict(v)
        self.modelIndex = int(index)
        print("the model index is " + str(self.modelIndex))
        return self.questionsPattern[str(self.modelIndex)]
