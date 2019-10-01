from skimage import data
from skimage.viewer import ImageViewer
from skimage.io import imread
from skimage import feature
from skimage.transform import (hough_line, hough_line_peaks, probabilistic_hough_line)
from skimage.filters import threshold_otsu, threshold_adaptive
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from skimage import exposure
from skimage import filters
import math

def first_nonzero(arr, axis, invalid_val=-1):
    mask = arr!=0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

def last_nonzero(arr, axis, invalid_val=-1):
    mask = arr!=0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


image = imread(r'D:\\victoria_edges\\3.jpg', as_gray=True)
#image = threshold_adaptive(image,51,offset=0.1)


canny_edges =  feature.canny(image, sigma=5)
sobel_edges = filters.sobel_h(image)
sobel_edges = threshold_adaptive(sobel_edges,51,offset=0.1)
plt.imshow(sobel_edges)
plt.show()
# straight-line Hough transform on the canny edges
h, theta, d = hough_line(sobel_edges)

plt.imshow(image, cmap=cm.gray)
m = 0
c=[]

for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
    m=(y0-y1)/image.shape[1] #based on the cartesian line eqn y=mx+c
    c.append( y1-m*image.shape[1]) # based on the cartesian line eqn y=mx+c
    plt.plot((0, image.shape[1]), (y0, y1), '-r')

    
plt.show()
distance = 0
if len(c) ==2:
    distance = (abs(c[1]-c[0]))/((m**2+1)**0.5) #distance between two parallel lines sharing same m. (y = mx+c)
if distance < 50 or len(c) ==1:
    #find the max vertical width of adaptive thresholded image
    #actual distance between edges = max vert width*cos (tan inverse of(m))
    image = threshold_adaptive(image,51,offset=0.1)
    image = np.invert(image)
    image = image.astype(int)
    distance_arr = []  
    first_nonzero_index_arr = []
    last_nonzero_index_arr = []  
    for i in range(0, image.shape[1]):
        column = image[:, i]
        first_nonzero_index_arr.append(first_nonzero(column, 0))
        last_nonzero_index_arr.append(last_nonzero(column, 0))
        
    distance = np.mean(first_nonzero_index_arr)-np.percentile(last_nonzero_index_arr,90)#use the 90 th percentile instead of max to prevent outlier effect
    distance = math.cos(np.arctan(m))*distance
else:
    print("couldn't find any edges")

print (distance)

