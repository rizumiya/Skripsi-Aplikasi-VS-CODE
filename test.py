from email import utils
from json import tool
import cv2
import numpy as np
import assets.libs.utlis as utlis

# ===============================
path = "assets/paper/paper.jpg"
widthImg = 600
heightImg = 800
# ===============================

img = cv2.imread(path)

# Preprocessing===========================================
img = cv2.resize(img, (widthImg, heightImg))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)



imgArray = ([img, imgGray, imgBlur, imgCanny])
imgStacked = utlis.stackImages(imgArray, 0.5)

cv2.imshow("Stacked Images", imgStacked)
cv2.waitKey(0)
