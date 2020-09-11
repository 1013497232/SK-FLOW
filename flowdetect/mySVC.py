import joblib
from sklearn import svm
from sklearn.metrics import confusion_matrix, classification_report
import warnings


def kernelTest(kernel):
    if kernel == "linear":
        # 线性算法表现在poly和rbf之间，时间也很长。
        C = 5
        study = svm.SVC(kernel="linear", C=C)
    elif kernel == "rbf":
        # rbf算法通常表现不错，时间也不长，但是准确率不太稳定（推荐）
        C = 93
        gamma = 0.01
        study = svm.SVC(kernel="rbf", C=C, gamma=gamma)
    elif kernel == "poly":
        # poly算法表现最好，但是时间也最长
        C = 95
        coef0 = 20
        degree = 3
        gamma = 10
        study = svm.SVC(kernel="poly", C=C, coef0=coef0, degree=degree, gamma=gamma)
    elif kernel == "sigmoid":
        # sigmoid算法表现最差，r2l和u2r难以判断出来
        C = 100
        coef0 = 0
        gamma = 0.0001
        study = svm.SVC(kernel="sigmoid", C=C, coef0=coef0, gamma=gamma)
    else:
        warnings.warn("输入的内核未经参数调优或有误，将使用默认内核和参数！")
        study = svm.SVC(kernel='rbf')
    return study


class mySVC:

    def __init__(self, x_train, y_train, x_test, y_test, kernel="sigmoid", isJoblib=False):
        self.study = kernelTest(kernel)
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.isJoblib = isJoblib

    def train(self):
        self.study.fit(self.x_train, self.y_train)
        joblib.dump(self.study, 'pkls/svc.pkl')

    def show(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/svc.pkl')
        y_pred = self.study.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))
        # print(y_pred)

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/svc.pkl')
        y_pred = self.study.predict(self.x_test)
        print(y_pred)
        with open('svc_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')