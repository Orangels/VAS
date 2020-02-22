import cv2
import numpy as np
import base64
import time


aaa = np.array([1, 2])

test_img = cv2.imread('P001067.png', cv2.IMREAD_GRAYSCALE)
print(test_img.shape[:2])
time_load_start = time.time()
im = np.load('mask.npy')
im = im.astype(np.uint8)
# im = test_img
time_load_end = time.time()
print('load cost {}'.format(time_load_end - time_load_start))

time_save_start = time.time()
np.save('/Users/liusen/Documents/sz/智慧工地/Vas/static/test.npy', im)
time_save_end = time.time()
print('save cost {}'.format(time_save_end-time_save_start))


im_re = cv2.resize(im, (int(im.shape[1]*1.5), int(im.shape[0]*1.5)), interpolation=cv2.INTER_LINEAR)
im_re = cv2.resize(im_re, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_LINEAR)
print((im==im_re).all())

# cv2.imshow('ori', im)
# cv2.imshow('resize', im_re)
# cv2.waitKey(0)

# im = im.astype(np.int64)
# shape = im.shape
#
# img_str = im.tostring()
#
# _, enc = cv2.imencode('.jpg', im)
# enc_str = enc.tostring()
# enc_b = np.fromstring(enc_str, np.uint8)
# enc_c = cv2.imdecode(enc_b, cv2.IMREAD_GRAYSCALE)
#
# img_b = np.fromstring(img_str, np.int64)
# img_b = img_b.reshape(shape)
# # print(img_str)
# print((im==enc_c).all())
# # print(im == enc_c)
# a = (im == enc_c)
# mask2_coor = np.where(a == 0)
# c = np.where(a == False)
# print(1)