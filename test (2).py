import sys
import cv2 as cv

cv.samples.addSamplesDataSearchPath('C:\Program Files\opencv\sources\samples\data')

img = cv.imread(cv.samples.findFile('starry_night.jpg'))

cv.imshow("Display window", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite()
