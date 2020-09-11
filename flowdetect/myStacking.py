import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import StackingClassifier, RandomForestClassifier


# get a stacking ensemble of models
def get_stacking():
    # define the base models
    level0 = list()
    level0.append(('lr', LogisticRegression())) #逻辑回归
    level0.append(('knn', KNeighborsClassifier()))  # K邻近
    level0.append(('rf', RandomForestClassifier())) # 随机森林
    level0.append(('bayes', GaussianNB()))  # 朴素贝叶斯
    # define meta learner model
    level1 = LogisticRegression()   # 用逻辑回归算法作为元模型
    # define the stacking ensemble
    model = StackingClassifier(estimators=level0, final_estimator=level1, cv=5)
    return model

# 堆叠算法
class myStacking:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib  # 由用户决定现场训练数据还是使用之前训练好的模型，默认不使用训练好的模型
        self.stacking = get_stacking()

    def train(self):  # 重新训练模型并保存，方便下次直接使用
        self.stacking.fit(self.x_train, self.y_train)
        joblib.dump(self.stacking, 'pkls/stacking.pkl')

    def show(self):
        if self.isJoblib is True:  # 使用之前训练好的模型
            self.stacking = joblib.load('pkls/stacking.pkl')
        y_pred = self.stacking.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def excute(self):  # 外层函数最终需要调用的方法
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.stacking = joblib.load('pkls/stacking.pkl')
        y_pred = self.stacking.predict(self.x_test)
        print(y_pred)
        with open('stacking_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')
