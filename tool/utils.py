import json
import cv2
import numpy as np
import os


def process_seg_result(filePs=None, seg_param=[], segpx=0, segopt=-1, seg_mask=None):
    """
    :param filePs:
    :param seg_param: seg 检测区域
    :param segpx: 0: 不返回 seg 坐标, 1: 返回坐标
    :param segopt: -1 不返回覆盖比, 0: 覆盖部分覆盖比 1: 裸露部分覆盖比
    :param seg_mask: mask numpy 转的 str
    :return:
    """
    npy_path = transform_extension_path(filePs)
    # 原图
    # img = cv2.imread(filePs)
    # seg 分析后的 mask
    seg_mask = np.load(npy_path)

    print('utils seg_param {}'.format(seg_param))
    mask_rois = get_roi(seg_mask, seg_param)

    result_arr = []
    for index, lsPointsChoose in enumerate(seg_param):
        if len(lsPointsChoose) == 2:
            img_area = (lsPointsChoose[1][0]-lsPointsChoose[0][0]) * (lsPointsChoose[1][1]-lsPointsChoose[0][1])
        elif len(lsPointsChoose) > 2:
            pts = np.array([lsPointsChoose], np.int32)
            # pts.shape=(点个数，2)
            pts = pts.reshape((-1, 1, 2))  # -1代表剩下的维度自动计算
            img_area = cv2.contourArea(pts)
        mask_roi = mask_rois[index]
        if segopt == 0:
            # 返回覆盖部分
            mask_segopt = np.where(mask_roi == 1)
            mask_area = mask_segopt[0].shape[0]
            # 覆盖比
            ratio = int(mask_area / img_area * 100)
            if segpx:
                c_list = []
                for i in range(len(mask_segopt)):
                    c_list.append(mask_segopt[i].reshape(-1, 1))
                # 坐标
                mask_coor = np.hstack((c_list[0], c_list[1]))
                mask_coor = mask_coor.tolist()
                result_arr.append(dict(ratio=ratio, pixels=mask_coor))
            else:
                result_arr.append(dict(ratio=ratio, pixels=[]))
        elif segopt == 1:
            # 返回裸露部分
            mask_segopt = np.where(mask_roi == 2)
            mask_area = mask_segopt[0].shape[0]
            # 覆盖比
            ratio = int(mask_area / img_area * 100)
            if segpx:
                c_list = []
                for i in range(len(mask_segopt)):
                    c_list.append(mask_segopt[i].reshape(-1, 1))
                # 坐标
                mask_coor = np.hstack((c_list[0], c_list[1]))
                mask_coor = mask_coor.tolist()
                result_arr.append(dict(ratio=ratio, pixels=mask_coor))
            else:
                result_arr.append(dict(ratio=ratio, pixels=[]))
    os.remove(npy_path)
    return result_arr


def get_roi(img, seg_params):
    # lsPointsChoose = [(30, 45), (100, 15), (100, 15), (330, 240), (50, 250)]
    img_arr = []
    for lsPointsChoose in seg_params:
        mask = np.zeros(img.shape, np.uint8)
        if len(lsPointsChoose) == 2:
            # h * w
            mask[lsPointsChoose[0][1]:lsPointsChoose[1][1], lsPointsChoose[0][0]:lsPointsChoose[1][0]] = img[lsPointsChoose[0][1]:lsPointsChoose[1][1], lsPointsChoose[0][0]:lsPointsChoose[1][0]]
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
            img_arr.append(ROI)
    return img_arr


def transform_extension_path(path, extension='.npy'):
    file = os.path.basename(path)
    dir_name = os.path.dirname(path)
    file_name, extension_name = os.path.splitext(file)
    file_name = file_name + extension
    result_path = os.path.join(dir_name, file_name)
    return result_path


def color_encode(labelmap, colors, mode='RGB'):
    labelmap = labelmap.astype('int')
    labelmap_rgb = np.zeros((labelmap.shape[0], labelmap.shape[1], 3),
                            dtype=np.uint8)
    for label in np.unique(labelmap):
        if label < 0:
            continue
        labelmap_rgb += (labelmap == label)[:, :, np.newaxis] * \
                        np.tile(colors[label],
                                (labelmap.shape[0], labelmap.shape[1], 1))

    if mode == 'BGR':
        return labelmap_rgb[:, :, ::-1]
    else:
        return labelmap_rgb


if __name__ == '__main__':
    # print(transform_extension_path('/Users/liusen/Documents/sz/智慧工地/Vas/test/test_seg.png'))
    # img = cv2.imread('/Users/liusen/Documents/sz/智慧工地/Vas/test/P000014.png')
    # seg_mask = np.load('/Users/liusen/Documents/sz/智慧工地/Vas/test/mask.npy')
    # seg_mask = seg_mask.astype(np.uint8)
    # from scipy.io import loadmat
    #
    # colors = loadmat('/Users/liusen/Documents/sz/智慧工地/Vas/test/color150.mat')['colors']
    # pred_color = color_encode(seg_mask, colors)
    # im_vis = np.concatenate((img, pred_color),
    #                         axis=1).astype(np.uint8)
    # # get_roi(seg_mask, [[(0, 0), (700, 500)], [(700, 0), (1400, 1000)]])
    # cv2.imshow('test', pred_color)
    # cv2.waitKey(0)

    seg_mask = np.load('/Users/liusen/Documents/sz/智慧工地/Vas/test/mask.npy')
    result = process_seg_result(filePs='/Users/liusen/Documents/sz/智慧工地/Vas/test/P000014.png',
                       seg_param=[[(0, 0), (700, 500)], [(700, 0), (1400, 1000)]],
                       segpx=1,
                       segopt=0,
                       seg_mask=None)
    print(1)