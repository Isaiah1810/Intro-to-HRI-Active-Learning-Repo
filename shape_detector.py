import cv2
import numpy as np
#Pink, yellow, green, orange


def pink_thresh(img):
    result = img.copy()
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 40, 20])
    upper1 = np.array([10, 180, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([150,40,20])
    upper2 = np.array([179,180,255])

    lower_mask = cv2.inRange(hsv_img, lower1, upper1)
    upper_mask = cv2.inRange(hsv_img, lower2, upper2)
    full_mask = lower_mask + upper_mask
    result = cv2.bitwise_and(result, result, mask=full_mask)
    return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

def green_thresh(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([40, 30, 20])
    upper = np.array([75, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)
    return mask

def yellow_thresh(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([25, 30, 20])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)
    return mask

def orange_thresh(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([15, 200, 20])
    upper = np.array([22, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)
    return mask

def detect_shapes(mask):
    # cv2.imshow("mask",mask)
    # cv2.waitKey()
    conts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    conts = sorted(conts, key=cv2.contourArea, reverse=True)
    shapes = []
    for c in conts:
        area = cv2.contourArea(c)
        if (area>200):
            peri1 = cv2.arcLength(c, True)
            approx1 = cv2.approxPolyDP(c, 0.02*peri1, True)
            # print(len(approx1))
            shapes.append(len(approx1))
    return shapes

def get_shapes(img):
    pink_mask = pink_thresh(img)
    orange_mask = orange_thresh(img)
    green_mask = green_thresh(img)
    yellow_mask = yellow_thresh(img)
    pink_shapes = detect_shapes(pink_mask)
    orange_shapes = detect_shapes(orange_mask)
    green_shapes = detect_shapes(green_mask)
    yellow_shapes = detect_shapes(yellow_mask)
    print("Pink shapes are", pink_shapes)
    print("Orange shapes are", orange_shapes)
    print("Green shapes are", green_shapes)
    print("Yellow shapes are", yellow_shapes)

img = cv2.imread("shapes.jpg")
get_shapes(img)