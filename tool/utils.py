import json
import cv2
import numpy as np


def process_seg_result(filePs=None, seg_param=[], segpx=0, segopt=-1, seg_mask=None):
    """
    :param filePs:
    :param seg_param: seg 检测区域
    :param segpx: 0: 不返回 seg 坐标, 1: 返回坐标
    :param segopt: -1 不返回覆盖比, 0: 覆盖部分覆盖比 1: 裸露部分覆盖比
    :param seg_mask: mask numpy 转的 str
    :return:
    """
    img_arr = get_roi(filePs, seg_param)
    #TODO seg 逻辑
    return [dict(filePs=filePs, seg_param=seg_param, segpx=segpx, segopt=segopt, seg_mask=seg_mask)]


def get_roi(img_path, seg_params):
    # lsPointsChoose = [(30, 45), (100, 15), (100, 15), (330, 240), (50, 250)]
    img_arr = []
    for lsPointsChoose in seg_params:
        img = cv2.imread(img_path)
        mask = np.zeros(img.shape, np.uint8)
        if len(lsPointsChoose) == 2:
            # h * w
            mask[lsPointsChoose[0][1]:lsPointsChoose[1][1], lsPointsChoose[0][0]:lsPointsChoose[1][0]] = img[lsPointsChoose[0][1]:lsPointsChoose[1][1], lsPointsChoose[0][0]:lsPointsChoose[1][0]]
            # cv2.imwrite('/Users/liusen/Documents/sz/智慧工地/Vas/test/{}.jpg'.format(lsPointsChoose[0][0]), mask)
            img_arr.append(mask)
        elif len(lsPointsChoose) > 2:
            pts = np.array([lsPointsChoose], np.int32)
            # pts.shape=(5，2)
            pts = pts.reshape((-1, 1, 2))  # -1代表剩下的维度自动计算
            # reshape 后的 pts.shape=(5。1，2)？？
            # --------------画多边形---------------------
            mask = cv2.polylines(mask, [pts], True, (0, 255, 255))
            ##-------------填充多边形---------------------
            mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))
            # cv2.imshow('mask', mask2)
            ROI = cv2.bitwise_and(mask2, img)
            # cv2.imshow('ROI', ROI)
            # cv2.waitKey(0)
            # cv2.imwrite('/Users/liusen/Documents/sz/智慧工地/Vas/test/{}.jpg'.format(lsPointsChoose[0][0]), ROI)
            img_arr.append(mask)
    return img_arr