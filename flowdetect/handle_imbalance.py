import imblearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import pyplot
import matplotlib
from imblearn.combine import SMOTEENN,SMOTETomek
from imblearn.under_sampling import OneSidedSelection
from sklearn.decomposition import PCA


'''
def handleLabel(input):
    label_list = ['dos','normal', 'scan', 'u2r', 'r2l']
    return label_list.index(input)
'''
def plot_2d_space(X,y, label='Classes'):

    colors = ['black', 'blue', 'purple', 'yellow','red']
    markers = ['o', '4','1','2','3']
    for l, c, m in zip(np.unique(y), colors, markers):
        plt.scatter(
            X[y==l, 0],
            X[y==l, 1],
            c=c, label=l, marker=m
        )
    plt.title(label)
    plt.legend(loc='upper right')
    plt.show()


## put no label datas in it
def preparation(path_NoLabel):

    file = pd.read_csv(path_NoLabel,sep=",")

    X = file.iloc[:,0:28]#!!!!
    y = file.iloc[:, 28]
    return X,y

class handle_imbalance:

    def __init__(self, path=None):
        self.path = path
    

    
    def use_OSSSMOTEENN(self):
        X,y = preparation(self.path)
##############################
        dy = pd.DataFrame(y)
        dy.value_counts().plot(kind='bar',title='Count(label)')
        plt.show()
#################################
        oss = OneSidedSelection(random_state = 42,n_jobs=-1,sampling_strategy="majority")
        X_res,y_res = oss.fit_sample(X,y)

        dy_res = pd.DataFrame(y_res)
        dy_res.value_counts().plot(kind='bar',title='Count(label)')
        plt.show()
##############################
        sme = SMOTEENN(random_state=42,n_jobs=-1)
        X_sme, y_sme = sme.fit_sample(X_res, y_res)

    #draw bar

        dy_sme = pd.DataFrame(y_sme)
        dy_sme.value_counts().plot(kind='bar',title='Count(label)')
        plt.show()

    #generate csv

        df=pd.concat([X_sme,pd.DataFrame(y_sme)],axis=1)

        df.to_csv(self.path.replace('.csv','_OSSSMOTEENN_Final_Test.csv') ,index = None,header=None,float_format='%.4f')
        
    ###the first line of data will be delete    


    ##########draw PCA
        pca = PCA(n_components=2)
        X_sme = pca.fit_transform(X_sme)
        plot_2d_space(X_sme,y_sme, 'SMOTE + ENN')

        return self.path.replace('.csv','_OSSSMOTEENN_Final_Test.csv')




# if __name__ == '__main__':
#     path ="++Final_Test++_pre.csv"
#     #draw_bar(path)
#     mhi = My_handle_imbalance(path)
#     mhi.use_OSSSMOTEENN()
#
#     #use_SMOTETomek(path)
#     #draw_origin(path)