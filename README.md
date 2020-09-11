# SK-FLOW

* 一个基于Python语言开源scikit-learn库开发的的机器学习工具

* 用于捕获离线的恶意行为数据包及其恶意行为并进行其恶意行为行为检测分析，并给出准确率和误报率

* 支持多种机器学习算法如：KNN、SVM、LogicRe、RF、Voting、Stacking

* 支持对原始数据集进行增广、预处理、标准归一化处理

* 支持基于PCA，t-SNE降维算法的可视化显示

* 支持针对已有模型对捕获的未知流量进行预测分析

  

## Background

信息安全课程设计小组作业



## Status

* 目前版本支持离线的数据包处理，需要对原始的WireShark捕获的数据包处理后手动加标签，将来会考虑用准确率高的机器学习算法对捕获数据包进行预测并加入标签，使得工具更加自动化

* 也会考虑推出GUI，提升用户友好度

  

## Features

* 数据集格式是KDD'99的包含28个特征的子集 

  * 省去了嵌入数据负载中因加密而无需分析的TCP连接的内容特征部分(共13种特征)

* 可识别的流量标签相对于KDD'99进行了更改

  * 将原有的39小类攻击特征重新分为5大类(normal、dos、scan、u2r、r2l)

    

## Main Components

#### 1. Sniffer

* 使用WireShark捕获后的数据包进行数据集的生成

#### 2. Feature_extractor

* 将.pcapng格式分析转换为包含特征标签集的.csv格式
  * 重建连接:识别相关连接和对话的关联数据包进行合并，构成特征1-9
  * 基于时间和主机的网络统计：统计当前连接记录与之前一段时间内的连接记录，识别其中的某些联系，作为特征提取

#### 3. DATA_init_ 

* One-Sided Selection剔除多数类样本中的噪声和边界样本
* 用Smote+ENN对数据进行增广，使得各类攻击类型数据数量平衡
* 标准化数据，消除特征间的差异性
* 归一化数据，使得寻优过程变得平缓高效

#### 4. Scikit-learn

* train_test_split 分离数据集为训练集和测试集
* joblib 对训练好的模型进行保存加载
* 各种机器学习算法

#### 5. Train

* 选择不同算法训练数据集

#### 6. Show

* 加载已有的模型对给出测试集进行测试查看正确率和误报率

#### 7. Predict/Classify

* 对未给出分类的攻击类型进行机器学习预测分类

#### 8. Visualization

* 对数据集进行特征降维在二维上聚类可视化

  

## Install

### constructure
    │  all_title_re.csv
    │  flow_detect.py
    │  requirements.txt
    │  tree.txt
    │  
    ├─flowdetect
    │      all_title_re.csv
    │      Class_DATA_init.py
    │      data_handling.py
    │      handle_imbalance.py
    │      myKnn.py
    │      MyLogiRe.py
    │      myRf.py
    │      myStacking.py
    │      mySVC.py
    │      myVoting.py
    │      vis.py
    │      __init__.py
    │      
    ├─pkls
    │      knn.pkl
    │      LogiRe.pkl
    │      rf.pkl
    │      stacking.pkl
    │      svc.pkl
    │      voting.pkl
    │      
    └─svc_parameters
           girdsearch_poly.py
           girdsearch_rbf.py
           girdsearch_sigmoid.py
           gridsearch_linear.py


下载并创建本地项目即可



## Requirements

* pandas==1.1.1
* matplotlib==3.3.1
* numpy==1.19.1
* joblib==0.16.0
* imblearn==0.0
* scikit_learn==0.23.2





## Usage

**将所需数据集放在 flow_detect.py目录下**

**运行 flow_detect.py 并选择相应功能**

***(工具将会输出混淆矩阵以及准确率误报率矩阵，针对Predict预测内容进行输出并保存为.txt格式)***



## Update

### v1.0.0 (2020/9/11 12:30 +00:00)

* push的第一个版本



## Others

[KDD‘99 数据集下载](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)

[KDD’99_feature_extractor](https://github.com/AI-IDS/kdd99_feature_extractor)

[测试用数据集 *( 包含增广后数据 提取码: lbe2 )*](https://pan.baidu.com/s/1-QD2_9hba56NUw0Yk-y5hQ)







