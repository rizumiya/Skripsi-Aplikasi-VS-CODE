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

# Preprocessing
img = cv2.resize(img, (widthImg, heightImg))
imgContours = img.copy()
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

# Finding all contours
contours, hierarchy = cv2.findContours(
    imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

# Find Rectangles
rectCon = utlis.rectContour(contours)
biggestContour = utlis.getCornerPoints(rectCon[0])
gradePoints = utlis.getCornerPoints(rectCon[1])
# print(biggestContour)

if biggestContour.size != 0 and gradePoints.size != 0:
    cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
    cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 20)

    biggestContour = utlis.reorder(biggestContour)
    gradePoints = utlis.reorder(gradePoints)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32(
        [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    
    ptG1 = np.float32(gradePoints)
    ptG2 = np.float32(
        [[0, 0], [600, 0], [0, 800], [600, 800]])
    matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (600, 800))
    cv2.imshow("Grade", imgGradeDisplay)


imgBlank = np.zeros_like(img)
imgArray = ([img, imgGray, imgBlur, imgCanny],
            [imgContours, imgBiggestContours, imgWarpColored, imgBlank])
imgStacked = utlis.stackImages(imgArray, 0.5)

cv2.imshow("Stacked Images", imgStacked)
cv2.waitKey(0)
