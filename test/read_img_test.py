import cv2
import numpy as np
from PIL import Image
import time
path = '/home/user/workspace/priv-0220/privision_test/P000014.png'
num = 50


if __name__ == '__main__':
    sum_cv = 0
    sum_PIL = 0
    for i in range(num):
        print(i)
        time_start_cv = time.time()
        img_cv = cv2.imread(path)
        img_cv = img_cv[:, :, ::-1]
        time_over_cv = time.time()
        sum_cv += time_over_cv - time_start_cv

        time_PIL_start = time.time()
        img = Image.open(path).convert('RGB')
        time_PIL_over = time.time()
        sum_PIL += time_PIL_over-time_PIL_start


    print('cv cost arvg {}'.format(sum_cv/num))
    print('PIL cost arvg {}'.format(sum_PIL / num))