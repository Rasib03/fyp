import numpy as np
import cv2
def horizontalProjection(img):
    # Return a list containing the sum of the pixels in each row
    (h, w) = img.shape[:2]
    sumRows = []
    for j in range(h):
        row = img[j:j+1, 0:w]  # y1:y2, x1:x2
        sumRows.append(np.sum(row))
    return sumRows

def verticalProjection(img):
    # Return a list containing the sum of the pixels in each column
    (h, w) = img.shape[:2]
    sumCols = []
    for j in range(w):
        col = img[0:h, j:j+1]  # y1:y2, x1:x2
        sumCols.append(np.sum(col))
    return sumCols

def threshold(image, t):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, t, 255, cv2.THRESH_BINARY_INV)
    return image

def medianFilter(image, d):
    image = cv2.medianBlur(image, d)
    return image

def bilateralFilter(image, d):
    image = cv2.bilateralFilter(image, d, 50, 50)
    return image

def dilate(image, kernalSize):
    kernel = np.ones(kernalSize, np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    return image

def erode(image, kernalSize):
    kernel = np.ones(kernalSize, np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    return image