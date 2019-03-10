from skimage import io
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
from bresenham import bresenham
import pydicom
from pydicom.data import get_testdata_files


image = rgb2gray(io.imread('brain.jpg'))

height = image.shape[0]
width = image.shape[1]

# bresenham returns list of points 
# they are under the line ended in points x1, y1, x2, y2 (function arguments)
coordinates = list(bresenham(0,height-1,width-1,0))

for c in coordinates:
    image[c[0]][c[1]] = 1

plt.imshow(image, 'gray')
plt.show()

# DICOM files management
# ds = pydicom.dcmread("0015.DCM")
# print(ds.PatientName)
# plt.imshow(ds.pixel_array, cmap = 'gray') 
# plt.show()
