from scipy import misc
import numpy as np
import matplotlib.pyplot as plt

def radon(image, steps):
    R = np.zeros((steps, len(image)), dtype='float64')
    for s in range(steps):
        rotation = misc.imrotate(image, -s*180/steps).astype('float64')
        # print(rotation)
        R[:,s] = sum(rotation)
    return R/steps

image = misc.imread('brain.jpg', flatten=True).astype('float64')

radon = radon(image, image.shape[0])
# print(radon/630)
print(radon.shape)
plt.subplot(1, 2, 1), plt.imshow(image, cmap='gray')
plt.xticks([]), plt.yticks([])
plt.subplot(1, 2, 2), plt.imshow(radon, cmap='gray')
plt.xticks([]), plt.yticks([])
plt.show()