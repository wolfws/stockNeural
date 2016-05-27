#-*- coding: utf-8 -*-
import csv
import os

import pandas as pd

from tools.cm_plot import * #导入自行编写的混淆矩阵可视化函数


def predict(filename,type,indicator):
    neuralInputPath = 'data/neuralInput/' + filename + '/' + type + '/'
    neuralModelsPath = 'data/neuralModels/' + filename + '/' + type + '/'
    neuralOutputPath = 'data/neuralOutput/' + filename + '/' + type + '/'

    data = pd.read_excel(neuralInputPath + 'input' + indicator + '.xls')
    data = data.as_matrix()
    # shuffle(data)

    p = 0.8  # 设置训练数据比例
    train = data[:int(len(data) * p), :]
    test = data[int(len(data) * p):, :]

    from keras.models import Sequential  # 导入神经网络初始化函数
    from keras.layers.core import Dense, Activation, Dropout  # 导入神经网络层函数、激活函数

    if not os.path.exists(neuralModelsPath):
        os.mkdir(neuralModelsPath)
    netfile = neuralModelsPath+indicator+'.model'  # 构建的神经网络模型存储路径

    net = Sequential()  # 建立神经网络
    net.add(Dense(30, input_dim=28))  # 添加输入层（3节点）到隐藏层（10节点）的连接
    net.add(Activation('sigmoid'))  # 隐藏层使用relu激活函数
    net.add(Dense(40, activation='sigmoid'))  # 添加隐藏层、隐藏层的连接
    net.add(Dropout(0.5))
    net.add(Dense(1))  # 添加隐藏层（10节点）到输出层（1节点）的连接
    net.add(Activation('sigmoid'))  # 输出层使用sigmoid激活函数
    net.compile(loss='binary_crossentropy', optimizer='adam')  # 编译模型，使用adam方法求解

    if os.path.exists(neuralModelsPath+indicator+'.model'):
        net.load_weights(netfile)
    else:
        net.fit(train[:, 1:29], train[:, 29], nb_epoch=100, batch_size=1)  # 训练模型，循环1000次
        net.save_weights(netfile)  # 保存模型

    if type == 'binary':
        predict_result = net.predict_classes(test[:, 1:29]).reshape(len(test))  # 预测结果变形
        '''这里要提醒的是，keras用predict给出预测概率，predict_classes才是给出预测类别，而且两者的预测结果都是n x 1维数组，而不是通常的 1 x n'''

        cm_plot(test[:,29], predict_result).show() #显示混淆矩阵可视化结果

        from sklearn.metrics import roc_curve #导入ROC曲线函数
        import matplotlib.pyplot as plt

        predict_result2 = net.predict(test[:,1:29]).reshape(len(test))
        fpr, tpr, thresholds = roc_curve(test[:,29], predict_result2, pos_label=1)
        plt.plot(fpr, tpr, linewidth=2, label = 'ROC of LM') #作出ROC曲线
        plt.xlabel('False Positive Rate') #坐标轴标签
        plt.ylabel('True Positive Rate') #坐标轴标签
        plt.ylim(0,1.05) #边界范围
        plt.xlim(0,1.05) #边界范围
        plt.legend(loc=4) #图例
        plt.show() #显示作图结果
    elif type == 'real':
        predict_result = net.predict(test[:, 1:29]).reshape(len(test))  # 预测结果变形

    if not os.path.exists(neuralOutputPath):
        os.mkdir(neuralOutputPath)
    csvfile = file(neuralOutputPath + 'resultPredict' + indicator + '.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(predict_result)
    csvfile.close()