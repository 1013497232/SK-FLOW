import numpy as np
from sklearn import manifold, decomposition
from matplotlib import pyplot as plt
from sklearn.externals._arff import xrange


class vis:
    colors = ['black', 'blue', 'green', 'yellow', 'red']

    def __init__(self, X, y):
        self.X = X.values[0:1000,0:28]
        self.y = y.values[0:1000]

    def pre(self):
        label_list = ['normal', 'scan', 'dos', 'u2r', 'r2l']
        for i in range(len(self.y)):
            self.y[i] = label_list.index(self.y[i])

    def PCA(self):
        pca = decomposition.PCA(n_components=2, svd_solver='randomized')
        X_pca = pca.fit_transform(self.X)

        for i in xrange(len(vis.colors)):
            px = X_pca[:, 0][self.y == i]
            py = X_pca[:, 1][self.y == i]
            plt.scatter(px, py, c=vis.colors[i])
        plt.legend(np.arange(len(vis.colors)).astype(str))
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.savefig('PCA.png')
        plt.show()

    def t_SNE(self):
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=501)
        X_tsne = tsne.fit_transform(self.X)
        x_min, x_max = X_tsne.min(0), X_tsne.max(0)
        X_norm = (X_tsne - x_min) / (x_max - x_min)

        for i in range(X_norm.shape[0]):
            plt.text(X_norm[i, 0], X_norm[i, 1], str(self.y[i]), color=vis.colors[self.y[i]],
                     fontdict={'weight': 'bold', 'size': 9})
        plt.legend(np.arange(len(vis.colors)).astype(str))
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.savefig('t-SNE.png')
        plt.show()

    def solve(self):
        vis.pre(self)
        #vis.PCA(self)
        vis.t_SNE(self)

