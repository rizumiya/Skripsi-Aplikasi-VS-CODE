import cv2
import numpy as np
import assets.libs.utlis as utlis

# ===============================
path = "assets/paper/paper4.jpg"
widthImg = 600
heightImg = 800
kernel = np.ones((5, 5), np.uint8)

questions = 10
choices = 5

ans = [2, 3, 1, 2, 3, 2, 2, 3, 1, 3]

webcamFeed = True
cameraNo = 0
# ===============================

cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)

while True:
    if webcamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(path)
    # img = cv2.imread(path)
    # Preprocessing
    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgFinal = img.copy()
    imgBiggestContours = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 40)
    imgDilate = cv2.dilate(imgCanny, kernel, iterations=1)
    # imgCanny = imutils.auto_canny(imgBlur)

    try:

        # Finding all contours
        contours, hierarchy = cv2.findContours(
            imgDilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        # Find Rectangles
        rectCon = utlis.rectContour(contours)
        biggestContour = utlis.getCornerPoints(rectCon[0])
        gradePoints = utlis.getCornerPoints(rectCon[1])
        # print(biggestContour)

        if biggestContour.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imgBiggestContours,
                             biggestContour, -1, (0, 255, 0), 20)
            cv2.drawContours(imgBiggestContours,
                             gradePoints, -1, (255, 0, 0), 20)

            biggestContour = utlis.reorder(biggestContour)
            gradePoints = utlis.reorder(gradePoints)

            pt1 = np.float32(biggestContour)
            pt2 = np.float32(
                [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(
                img, matrix, (widthImg, heightImg))

            ptG1 = np.float32(gradePoints)
            ptG2 = np.float32(
                [[0, 0], [600, 0], [0, 800], [600, 800]])
            matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (600, 800))
            # cv2.imshow("Grade", imgGradeDisplay)

            # Apply Treshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgTresh = cv2.threshold(
                imgWarpGray,  130, 255, cv2.THRESH_BINARY_INV)[1]
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
                if countC == 0:
                    myPixelVal[countR][countC] = 0
                else:
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
                # print(myIndex)

            # Grading
            grading = []
            for x in range(0, questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            # print(grading)
            score = (sum(grading)/questions) * 20  # 1 nilai = 2
            print(score)

            # Displaying correct answers
            imgResult = imgWarpColored.copy()
            utlis.showAnswers(imgResult, myIndex, grading,
                              ans, questions, choices)
            imgRawDrawing = np.zeros_like(imgWarpColored)
            utlis.showAnswers(imgRawDrawing, myIndex, grading,
                              ans, questions, choices)
            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInWarp = cv2.warpPerspective(
                imgRawDrawing, invMatrix, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, imgInWarp, 1, 0)
            cv2.putText(imgFinal, str(int(score)), (25, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 3, (50, 255, 100), 4)
            # cv2.imshow("Grade", imgRawGrade)

        imgBlank = np.zeros_like(img)
        imgArray = ([img, imgGray, imgBlur, imgCanny],
                    [imgContours, imgBiggestContours, imgWarpColored, imgTresh])

    except:
        imgBlank = np.zeros_like(img)
        imgArray = ([img, imgGray, imgBlur, imgDilate],
                    [imgBlank, imgBlank, imgBlank, imgBlank])

    imgStacked = utlis.stackImages(imgArray, 0.5)
    cv2.imshow("Final Grade", imgFinal)

    cv2.imshow("Stacked Images", imgStacked)
    # cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("FinalResult.jpg", imgFinal)
        cv2.waitKey(0)
