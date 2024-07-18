
import cv2
import numpy as np

def stretch_columns(img):
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
    img = cv2.erode(img, structure, iterations=1)
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1,20))
    x = cv2.dilate(img, structure, iterations=2)
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
    x = cv2.dilate(x, structure, iterations=1)
    contours, hierarchy = cv2.findContours(x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imwrite("columnstretched.jpg", x)
    return x

def segment_columns(img, shape, contours):
    mask = np.zeros((shape[0], shape[1]), np.uint8)
    for key in contours:
        for i in contours[key]:
            [x, y, w, h] = i
            mask = cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
            print(y, " ", y + h, " ", x, " ", x + w, " is 255")

    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 1))
    mask = cv2.erode(mask, structure, iterations=1)
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
    mask = cv2.dilate(mask, structure, iterations=2)
    cont, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cont:
        [x, y, w, h] = cv2.boundingRect(c)
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 3)

    cv2.imwrite("blocks.jpg", img)
    return cont

def ignore_lines(image, save_dir, file_name):
    # Check if the image is already in grayscale
    if len(image.shape) == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges in the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Apply Hough Line Transform to find lines in the image
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Find contours in the image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Convert contours to a dictionary format
    contours_dict = {i: [cv2.boundingRect(cnt)] for i, cnt in enumerate(contours)}

    return contours, hierarchy, image

