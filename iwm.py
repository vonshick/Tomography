from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rescale
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
    emitter_coordinates = []
    detector_coordinates = []
    for i in range( steps ):
        angle = alpha * i
        print(angle)
        x_emitter = center[0] + int(radius * np.cos(angle))
        y_emitter =  center[1] + int(radius * np.sin(angle))
        emitter_coordinates.append((x_emitter, y_emitter))
        detector_coordinates.append([])

        for j in range(detectors_count):
            x = center[0] + int(radius * np.cos(angle + np.pi - arc/2 + j * arc/(detectors_count-1)))
            y = center[1] + int(radius * np.sin(angle + np.pi - arc/2 + j * arc/(detectors_count-1)))
            coordinates = list(bresenham(x_emitter, y_emitter, x, y))
            detector_coordinates[i].append((x,y))
            
            for c in coordinates:
                if c[0] < height and c[1] < width and c[0] >= 0 and c[1] >= 0: 
                    image[c[0], c[1]]= 1
                    sinogram[j, i] += image[c[0], c[1]]
                    pixels_lines_count[c[0], c[1]] += 1

    return sinogram , pixels_lines_count, emitter_coordinates, detector_coordinates, image

def reverse_radon(sinogram, pixels_lines_count, emitters, detectors):
    image = np.array([])
    detectors_count = sinogram.shape[0]
    steps = sinogram.shape[1]
    height = pixels_lines_count.shape[0]
    width = pixels_lines_count.shape[1]
    print("Detectors count: "+detectors_count)
    print("Steps: " + steps)
    print("Image height: "+height)
    print("Image width: "+width)

    image = np.zeros(( height, width ))
    
    for i in range( steps ):
        print(i)
        for j in range(detectors_count):
            coordinates = list(bresenham(emitters[i][0], emitters[i][1], detectors[i][j][0], detectors[i][j][1]))
            for c in coordinates:
                if c[0] < height and c[1] < width and c[0] >= 0 and c[1] >= 0: 
                    image[c[0], c[1]] += sinogram[j, i] / pixels_lines_count[c[0], c[1]]
    return image 

def normalize_image(image):
    max = np.max(image)
    min = np.min(image)
    normalized_image = np.zeros((1, image.shape[1]))
    for i in range(image.shape[0]):
        if i == 0:
            normalized_image[i,:] += [(x-min)/(max-min) for x in image[i,:]]
        else:
            normalized_image = np.vstack(( normalized_image, [(x-min)/(max-min) for x in image[i,:]] ))
    return normalized_image

def main():
    image = rgb2gray(io.imread('brain.jpg'))
    image = rescale(image, 1.0 / 5.0, anti_aliasing=False)
    
    alpha = np.pi/180
    arc = np.pi/12
    detectors_count = 100

    sinogram, pixels_lines_count, emitter_coordinates, detector_coordinates, image  = radon(alpha,arc,detectors_count, image)
    plt.imshow(image, 'gray')
    plt.show()
    # sinogram = normalize_image(sinogram)    
    # io.imsave( 'sinogram.png', sinogram)
    plt.imshow(sinogram, 'gray')
    plt.show()


    image = reverse_radon(sinogram, pixels_lines_count, emitter_coordinates, detector_coordinates)
    plt.imshow(image, 'gray')
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