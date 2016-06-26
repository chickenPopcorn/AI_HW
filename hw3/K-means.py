import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
import matplotlib.pyplot as plt
import sklearn.cluster
import scipy
from sklearn.utils import shuffle

def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image


if __name__ == '__main__':

    image = scipy.misc.imread('trees.png')
    image = np.array(image, dtype=np.float64) / 255
    w, h, d = original_shape = tuple(image.shape)
    image_array = np.reshape(image, (w * h, d))
    image_array_sample = shuffle(image_array)[:1000]
    kmeans = KMeans(n_clusters=3).fit(image_array_sample)
    labels = kmeans.predict(image_array)
    codebook_random = shuffle(image_array)[:3 + 1]
    labels_random = pairwise_distances_argmin(codebook_random, image_array, axis=0)

    plt.clf()
    ax = plt.axes([0, 0, 1, 1])
    plt.axis('off')
    plt.title('Quantized image (3 colors, K-Means)')
    plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))
    plt.savefig('output.png')
