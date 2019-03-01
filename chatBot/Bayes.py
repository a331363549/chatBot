__author__ = 'ding'
'''
朴素贝叶斯类
'''
import math
import random


class NaiveBayesModel:

    def splitDataset(self, dataset, splitRatio):
        trainSize = int(len(dataset) * splitRatio)
        trainSet = []
        copy = list(dataset)
        while len(trainSet) < trainSize:
            index = random.randrange(len(copy))
            trainSet.append(copy.pop(index))
        return [trainSet, copy]

    # 将样本最后一个值作为该样本的映射
    # 按类别划分数据
    def separateByClass(self, dataset):
        separated = {}
        for i in range(len(dataset)):
            vector = dataset[i]
            if vector[-1] not in separated:
                separated[vector[-1]] = []
            separated[vector[-1]].append(vector)
        return separated

    # 计算均值
    def mean(self, numbers):
        return sum(numbers) / float(len(numbers))

    def stdev(self, numbers):
        avg = self.mean(numbers)
        variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
        return math.sqrt(variance)

    # 提取数据集特征
    def summarize(self, dataset):
        summaries = [(self.mean(attribute), self.stdev(attribute)) for attribute in zip(*dataset)]
        del summaries[-1]
        return summaries

    # 按类别提取属性值
    def summarizeByClass(self, dataset):
        separated = self.separateByClass(dataset)
        summaries = {}
        for classValue, instances in separated.items():
            summaries[classValue] = self.summarize(instances)
        return summaries

    # 计算高斯概率密度函数
    def calculateProbability(self, x, mean, stdev):
        exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
        return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

    # 计算所属类的概率
    def calculateClassProbabilities(self, summaries, inputVector):
        probabilities = {}
        new_summaries = dict()
        new_vector = []
        for item in summaries:
            if item.label in new_summaries.keys():
                new_vector.append(list(item.features))
                new_summaries[item.label] = new_vector
            else:
                print(len(new_vector))
                new_vector = []
                new_summaries[item.label] = new_vector
        for classValue, classSummariesin in new_summaries.items():
            probabilities[classValue] = 1
            for i in range(len(summaries[0].features)):
                mean = self.mean(inputVector)
                stdev = self.stdev(inputVector)
                x = inputVector[i]
                probabilities[classValue] *= self.calculateProbability(x, mean, stdev)
        return probabilities

    # 单一预测
    def predict(self, summaries, inputVector):
        probabilities = self.calculateClassProbabilities(summaries, inputVector)
        bestLabel, bestProb = None, -1
        for classValue, probability in probabilities.items():
            if bestLabel is None or probability > bestProb:
                bestProb = probability
                bestLabel = classValue
        return bestLabel
