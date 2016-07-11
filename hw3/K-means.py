import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import scipy


if __name__ == '__main__':
    image = scipy.misc.imread('trees.png')
    image = np.array(image, dtype=np.float64) / 255
    w, h, d = original_shape = tuple(image.shape)
    image_array = np.reshape(image, (w * h, d))

    labels = KMeans(n_clusters=3).fit(image_array).predict(image_array)
    newImage = np.zeros((w, h, d))
    count = 0
    for i in range(w):
        for j in range(h):
            newImage[i][j] = image_array[labels[count]]
            count += 1
    plt.clf()
    plt.title("K=3")
    plt.imshow(newImage)
    plt.show()
