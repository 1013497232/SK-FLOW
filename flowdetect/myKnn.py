import joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier


class myKnn:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib
        self.knn = KNeighborsClassifier(n_neighbors=5, weights='distance',
                                        algorithm='auto', leaf_size=30, p=1, metric='minkowski', metric_params=None,
                                        n_jobs=-1)

    def train(self):
        self.knn.fit(self.x_train, self.y_train)
        joblib.dump(self.knn, 'pkls/knn.pkl')

    def show(self):
        if self.isJoblib is True:
            self.knn = joblib.load('pkls/knn.pkl')
        y_pred = self.knn.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.knn = joblib.load('pkls/knn.pkl')
        y_pred = self.knn.predict(self.x_test)
        print(y_pred)
        with open('knn_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')
