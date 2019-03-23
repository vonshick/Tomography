from skimage import io
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
from bresenham import bresenham
import pydicom
import numpy as np
from math import floor, ceil, sqrt
# Questions
# 1. Does bresenham algorithm has to be implemented by ourselves? YES
# 2. What kind of patient's data can be editted by user? imie, nazwisko, PESEL
# 3. What about interactive notebook?
# 4. What kind of comments should be possible to comment in DICOM files? (ImageComments?)

# 5. Jak dziala sinogram?
# 6. Czy zrodlo moze byc rownolegle? (n emiterow i n detektorow)
# 7. Jakie średnie bierzemy pod uwagę? 
# 8. Normalizacja: rejestrujemy ILE!!! linii przechodzi przez dany punkt czy KTÓRE?

def count_image_parameters(image):
    height = image.shape[0]
    width = image.shape[1]
    center = ( floor( height/2 ), floor( width/2 ))
    pixels_lines_count = np.zeros((height, width))
    radius = ceil( sqrt(height**2 + width**2) / 2 )
    return height, width, center, radius, pixels_lines_count

def radon(alpha, arc, detectors_count, image):
    height, width, center,  radius, pixels_lines_count = count_image_parameters(image)
    steps = int( np.pi*2 / alpha)
    sinogram = np.zeros((detectors_count, steps))
    for j in range( steps ):
        print(j)
        angle = alpha * j
        x_emitter = center[0] + int(radius * np.cos(angle))
        y_emitter =  center[1] + int(radius * np.sin(angle))
        for i in range(detectors_count):
            x = center[0] + int(radius * np.cos(angle + np.pi - arc/2 + i * arc/(detectors_count-1)))
            y = center[1] + int(radius * np.sin(angle + np.pi - arc/2 + i * arc/(detectors_count-1)))
            coordinates = list(bresenham(x_emitter, y_emitter, x, y))
            # sum = 0
            for c in coordinates:
                if c[0] < height and c[1] < width and c[0] > 0 and c[1] > 0: 
                    sinogram[i][j] += image[c[0]][c[1]]
                    pixels_lines_count[c[0]][c[1]] += 1
    return sinogram, pixels_lines_count

def reverse_radon(arc, sinogram, pixels_lines_count):
    image = np.array([])
    detectors_count = sinogram.shape[0]
    steps = sinogram.shape[1]
    height = pixels_lines_count.shape[0]
    width = pixels_lines_count.shape[1]
    image = np.zeros(( height, width ))
    _, _, center, radius, _ = count_image_parameters(image)
    alpha = int(np.pi * 2/steps)

    part_of_argument = np.pi - arc/2
    for j in range( steps ):
        print(j)
        angle = alpha * j
        x_emitter = center[0] + int(radius * np.cos(angle))
        y_emitter =  center[1] + int(radius * np.sin(angle))
        for i in range(detectors_count):
            x = center[0] + int(radius * np.cos(angle + np.pi - arc/2 + i * arc/(detectors_count-1)))
            y = center[1] + int(radius * np.sin(angle + np.pi - arc/2 + i * arc/(detectors_count-1)))
            coordinates = list(bresenham(x_emitter, y_emitter, x, y))
            for c in coordinates:
                if c[0] < height and c[1] < width and c[0] > 0 and c[1] > 0: 
                    image[c[0]][c[1]] += sinogram[i][j] / pixels_lines_count[c[0]][c[1]]
    return image 
def main():
    image = rgb2gray(io.imread('brain.jpg'))
    
    alpha = np.pi/180
    arc = np.pi/3
    detectors_count = 160

    sinogram, pixels_lines_count = radon(alpha,arc,detectors_count, image)

    image_2 = reverse_radon(arc, sinogram, pixels_lines_count)

    plt.imshow(sinogram, 'gray')
    plt.show()

    plt.imshow(image_2, 'gray')
    plt.show()


main()




# # DICOM files management
# ds = pydicom.dcmread("0015.DCM")
# print(ds)
# print(ds.PatientName)
# print(ds.PatientID)
# print(ds.StudyDate)
# print(ds.ImageComments) 

# plt.imshow(ds.pixel_array, cmap = 'gray') 
# plt.show()