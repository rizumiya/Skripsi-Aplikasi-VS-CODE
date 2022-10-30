from email import utils
from json import tool
import cv2
import numpy as np
import assets.libs.utlis as utlis

# ===============================
path = "assets/paper/paper4.jpg"
widthImg = 600
heightImg = 800

questions = 10
choices = 5

ans = [2, 3, 1, 2, 3, 2, 2, 3, 1, 3]
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
biggestContour = utlis.getCornerPoints(rectCon[1])
gradePoints = utlis.getCornerPoints(rectCon[2])
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
    # cv2.imshow("Grade", imgGradeDisplay)

    # Apply Treshold
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgTresh = cv2.threshold(imgWarpGray,  130, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow("Grade", imgTresh)

    boxes = utlis.splitBoxes(imgTresh)
    # cv2.imshow("test", boxes[48])
    # print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))

    # Getting no  zero Pixel Values of each marks
    myPixelVal = np.zeros((questions, choices))
    countC = 0
    countR = 0

    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC] = totalPixels
        countC += 1
        if (countC == choices):
            countR += 1
            countC = 0
    print(myPixelVal)

    # Finding index values of the marks
    myIndex = []
    for x in range(0, questions):
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndex.append(myIndexVal[0][0])

    # Grading
    grading = []
    for x in range(0, questions):
        if ans[x] == myIndex[x]:
            grading.append(1)
        else:
            grading.append(0)
    print(grading)


imgBlank = np.zeros_like(img)
imgArray = ([img, imgGray, imgBlur, imgCanny],
            [imgContours, imgBiggestContours, imgWarpColored, imgTresh])
imgStacked = utlis.stackImages(imgArray, 0.5)

cv2.imshow("Stacked Images", imgStacked)
cv2.waitKey(0)
