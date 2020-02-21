import cv2
import numpy as np

image_path = 'test_seg.png'


if __name__ == '__main__':
    # img = cv2.imread('roi.jpg')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    #
    # binary, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    img = cv2.imread(image_path, 0)
    c = np.where(img == 255)
    c_list = []
    for i in range(len(c)):
        c_list.append(c[i].reshape(-1, 1))
    # 坐标
    aaa = np.hstack((c_list[0], c_list[1]))
    print(111)
