import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV


class myRf:
    def __init__(self, x_train, y_train, x_test, y_test, isJoblib=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.best_param = {'n_estimators': 51, 'max_features': 3}
        self.isJoblib = isJoblib

    # 对n_emistrators和max_features两个参数进行调优（网格搜索）
    def parameter_adjustment(self):
        # 调优n_estimators
        param_test1 = {"n_estimators": range(1, 101, 10)}
        g1 = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_test1, cv=10)
        g1.fit(self.x_train, self.y_train)
        print(g1.best_params_)
        print("best accuracy:%f" % g1.best_score_)
        self.best_param.update(g1.best_params_)

        # 调优max_features
        param_test2 = {"max_features": range(1, 11, 1)}
        g2 = GridSearchCV(estimator=RandomForestClassifier(n_estimators=g1.best_params_['n_estimators'],
                                                           random_state=10),
                          param_grid=param_test2, cv=10)
        g2.fit(self.x_train, self.y_train)
        print(g2.best_params_)
        print('best accuracy:%f' % g2.best_score_)
        self.best_param.update(g2.best_params_)

    def train(self):
        self.study = RandomForestClassifier(oob_score=True, random_state=10, n_jobs=-1,
                                            n_estimators=self.best_param['n_estimators'],
                                            max_features=self.best_param['max_features'])
        self.study.fit(self.x_train, self.y_train)
        joblib.dump(self.study, 'pkls/rf.pkl')

    # 利用随机森林对特征重要性进行评估
    def analysis_features(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/rf.pkl')
        file2 = pd.read_csv('all_title_re.csv')
        feat_labels = file2.columns[:-1]
        importances = self.study.feature_importances_
        indices = np.argsort(importances)[::-1]
        for f in range(28):
            print("%2d) %-*s %f" % (f + 1, 30, feat_labels[indices[f]], importances[indices[f]]))

    def show(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/rf.pkl')
        y_pred = self.study.predict(self.x_test)
        print(confusion_matrix(self.y_test, y_pred))
        print(classification_report(self.y_test, y_pred))

    def excute(self):
        if self.isJoblib is False:
            self.parameter_adjustment()
            self.train()
        self.analysis_features()
        self.show()

    def predict(self):
        if self.isJoblib is True:
            self.study = joblib.load('pkls/rf.pkl')
        y_pred = self.study.predict(self.x_test)
        print(y_pred)
        with open('rf_out.txt', 'w') as out:
            for i in y_pred:
                out.write(i+'\n')
