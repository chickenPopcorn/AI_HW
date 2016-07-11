from sklearn.cluster import KMeans
from sklearn.cluster import spectral_clustering
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler

# heavily reference the example from
# http://scikit-learn.org/stable/modules/clustering.html#spectral-clustering
# and was approved by TA

if __name__ == "__main__":
    plot_num = 1
    dataset = datasets.make_circles(n_samples=300, factor=.5, noise=.05)

    # prepare data
    X, y = dataset
    X = StandardScaler().fit_transform(X)

    spectral = cluster.SpectralClustering(n_clusters=2, eigen_solver='arpack', affinity="nearest_neighbors")
    kmeans = KMeans(n_clusters=2)

    clustering_algorithms = [kmeans, spectral]
    clustering_names = ['KMeans', 'Spectral Clustering']
    colors = ["red", 'blue']

    for name, algorithm in zip(clustering_names, clustering_algorithms):

            algorithm.fit(X)
            y_pred = algorithm.labels_.astype(np.int)

            # plot
            plt.subplot(2, 1, plot_num)
            plt.title(name, size=18)
            c = []
            for i in y_pred:
                c.append(colors[i])

            plt.scatter(X[:, 0], X[:, 1], color=c)

            if hasattr(algorithm, 'cluster_centers_'):
                # plot k-means center
                centers = algorithm.cluster_centers_
                center_colors = colors[:len(centers)]
                plt.scatter(centers[:, 0], centers[:, 1], s=100, c=center_colors)

            plt.xticks(())
            plt.yticks(())
            plot_num += 1

    plt.show()
