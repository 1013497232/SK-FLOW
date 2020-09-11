import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

# 投票算法（软投票）
class myVoting:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.isJoblib = isJoblib
        log_clf = LogisticRegression()
        rnd_clf = RandomForestClassifier()
        knn_clf = KNeighborsClassifier()
        self.voting_clf = VotingClassifier(
            estimators=[('lr', log_clf), ('rf', rnd_clf), ('knn', knn_clf)],
            voting='soft'
        )

    def train(self):
        self.voting_clf.fit(self.x_train, self.y_train)
        joblib.dump(self.voting_clf, 'pkls/voting.pkl')

    def show(self):
        if self.isJoblib is True:
            self.voting_clf = joblib.load('pkls/voting.pkl')
        y_pred = self.voting_clf.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def excute(self):
        if self.isJoblib is False:
            self.train()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.voting_clf = joblib.load('pkls/voting.pkl')
        y_pred = self.voting_clf.predict(self.x_test)
        print(y_pred)
        with open('voting_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')