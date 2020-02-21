import cv2
import numpy as np
import time

img_path = '/Users/liusen/Downloads/Kobe_1280_720.jpeg'
# img_path = 'test_seg.png'

if __name__ == '__main__':
    time_start = time.time()
    lsPointsChoose = [[(640, 0), (1279, 0), (1279, 360), (1000, 400), (700, 250)],
                      [(640, 0), (1279, 0), (1279, 360), (1000, 400), (700, 250)]]
    # lsPointsChoose = [(600, 100), (1200, 100), (1200, 700), (600, 700)]
    # lsPointsChoose = [(599, 101), (1201, 101), (1201, 701), (599, 701)]
    img = cv2.imread(img_path)
    for lsPointChoose in lsPointsChoose:
        time_read_img = time.time()
        mask = np.zeros(img.shape, np.uint8)
        pts = np.array([lsPointChoose], np.int32)
        # pts.shape=(5，2)
        pts = pts.reshape((-1, 1, 2))  # -1代表剩下的维度自动计算
        # reshape 后的 pts.shape=(5。1，2)？？
        # --------------画多边形---------------------
        mask = cv2.polylines(mask, [pts], True, (0, 255, 255))
        ##-------------填充多边形---------------------
        mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))

        # 计算面积
        # mask2 = mask2[:, :, 0]
        # mask2_coor = np.where(mask2 == 255)
        # roi_area = mask2_coor[0].shape[0]
        time_end = time.time()
        # cv2 计算面积
        area = cv2.contourArea(pts)
        length = cv2.arcLength(pts, True)
        # print(length)
        print('countour area {}'.format(area + length/2))
        # print('roi area {}'.format(roi_area))
        # print(time.time()-time_end)
        # print('read img cost {}'.format(time_read_img-time_start))
        # 这里的耗时主要在 计算坐标这里的耗时
        print('compute roi area cost {}'.format(time_end-time_read_img))

    # cv2.imshow('mask', mask2)
    # ROI = cv2.bitwise_and(mask2, img)
    # cv2.imshow('ROI', ROI)
    # cv2.waitKey(0)

