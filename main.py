######################################
######################################
############ Rowan Ashraf ############
############   Task 4.1   ############
############  Version 1.1 ############
######################################
######################################

# User guide:
#   four left clicks to choose a frame that transforms perspective according to chosen points(in any order)
#   'r' resets everything
#   Esc exits the program


import cv2
import numpy as np
import math

refPt = []
new = []
dis = []
cols = 0
rows = 0
n = 0
z = [0, 0, 0, 0]


def click_event(event, x, y, flags, params):
    global n
    # checks for a left click
    if event == cv2.EVENT_LBUTTONDOWN:
        # Put the clicks coordinates in a variable
        refPt.append([x, y])
        # put new values in a variable
        if len(refPt) > 4:
            new.append([x, y])
            # always renew values
            if len(new) == 4:
                n = 0
                refPt.clear()
                refPt.append([new[0][0], new[0][1]])
                refPt.append([new[1][0], new[1][1]])
                new.clear()


# make points in the correct order
def order():
    global n, cols, rows, z
    if n == 0:
        # top left corner
        for i in range(4):
            dis.append(math.sqrt(refPt[i][0]**2 + refPt[i][1]**2))
            if i > 0:
                if dis[i] < dis[z[0]]:
                    z[0] = i
            i += 1
        dis.clear()
        # top right corner
        for i in range(4):
            dis.append(math.sqrt(((refPt[i][0] - rows) ** 2) + (refPt[i][1] ** 2)))
            if i > 0:
                if dis[i] < dis[z[1]]:
                    z[1] = i
            i += 1
        dis.clear()

        # bottom right corner
        for i in range(4):
            dis.append(math.sqrt(((refPt[i][0] - rows) ** 2) + ((refPt[i][1] - cols) ** 2)))
            if i > 0:
                if dis[i] < dis[z[2]]:
                    z[2] = i
            i += 1
        dis.clear()

        # bottom left corner
        for i in range(4):
            dis.append(math.sqrt((refPt[i][0] ** 2) + ((refPt[i][1] - cols) ** 2)))
            if i > 0:
                if dis[i] < dis[z[3]]:
                    z[3] = i
            i += 1
        n = 1


def perspective_transform(frame):
    global cols, rows
    img = frame
    rows, cols = img.shape[0], img.shape[1]
    order()
    pts1 = np.float32([[refPt[z[0]][0], refPt[z[0]][1]], [refPt[z[1]][0], refPt[z[1]][1]], [refPt[z[3]][0], refPt[z[3]][1]], [refPt[z[2]][0], refPt[z[2]][1]]])
    pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
    m = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, m, (cols, rows))
    frame = dst
    return frame


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2.setMouseCallback("frame", click_event)
            if len(refPt) == 4:
                frame = perspective_transform(frame)
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k == ord('r'):
                refPt.clear()
                n = 0
                dis.clear()
                z = [0, 0, 0, 0]
    cv2.destroyAllWindows()