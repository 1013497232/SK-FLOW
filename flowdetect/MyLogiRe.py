import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from sklearn import manifold
from matplotlib import pyplot as plt

class MyLogiRe:
    def __init__(self, x_train, y_train, x_test, y_test,isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib
        self.study = LogisticRegression(solver='newton-cg', penalty='l2', max_iter=15000, tol=0.5)

    def train(self):
        self.study.fit(self.x_train, self.y_train)
        joblib.dump(self.study, 'pkls/LogiRe.pkl')

    def show(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/LogiRe.pkl')
        y_pred = self.study.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def show_image(self,prediction):
        def handleLabel(input):
            lable_list = ['normal','scan', 'dos', 'u2r', 'r2l']
            return lable_list.index(input)
        for i in prediction:
            prediction[i]=handleLabel(prediction[i])
        #降维
        tsne =manifold.TSNE(n_components=2, init = 'pca', random_state= 501)
        X_tsne = tsne.fit_transform(self.x_test)
        x_min, x_max = X_tsne.min(0), X_tsne.max(0)
        X_norm = (X_tsne - x_min) / (x_max - x_min)
        colors = ['black', 'blue', 'purple', 'yellow',  'red', 'lime', 'cyan', 'orange', 'gray','white']
        for i in range(X_norm.shape[0]):
            plt.text(X_norm[i, 0], X_norm[i, 1], str(prediction[i]), color=plt.cm.Set1(prediction[i]),
                     fontdict={'weight': 'bold', 'size': 9})
        plt.legend(np.arange(len(colors)).astype(str))
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.show()

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/LogiRe.pkl')
        y_pred = self.study.predict(self.x_test)
        print(y_pred)
        with open('LogiRe_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')
