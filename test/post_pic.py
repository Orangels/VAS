# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
import traceback

def uploadFile(log):
    url = 'http://127.0.0.1:9000/api/v1/detect'
    # files = {'file': open('D:/tmp/1.jpg', 'rb')}

    # headers = requests.utils.default_headers()
    # headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    # 要上传的文件
    # files = {'image_file': ('test.jpg', open('/Users/liusen/Downloads/Kobe.jpeg', 'rb'))
    # 		 }  # 显式的设置文件名
    #
    # # post携带的数据
    # data = {'type': '5',
    # 		'multiple': '1',
    # 		'new_interface':'1'
    # 		}
    time_total_para = 0
    time_total = 0
    time_algo = 0
    time_db = 0

    work_time = 0
    image_time = 0
    infer_time = 0
    singal_ssd_time = 0
    pose_time_total = 0
    reid_time_total = 0
    img_decode_time = 0
    time_begin = time.time()

    circle_num = 1
    detail_time = 0
    for i in range(circle_num):
        try:
            # car
            # files = {'img': ('P001067.png',
            #                         open('P001067.png',
            #                              'rb'))}  # 显式的设置文件名
            # fog
            # files = {'img': ('P000005.png',
            #                  open('P000005.png',
            #                       'rb'))}  # 显式的设置文件名
            
            # seg
            files = {'img': ('ht_test.jpg',
                             open('/home/user/workspace/priv-0220/Vas/test/0226_0.jpg',
                                  'rb'))}  # 显式的设置文件名
            # post携带的数据
            # data = dict(seg=[[0, 0, 1400, 500], [0, 500, 1400, 1000]], segpx=0, segopt=0, od=1)
            # data = dict(seg=[[0, 0, 500, 100], [0, 100, 500, 300]], segpx=0, segopt=0, od=1)
            data = dict(seg=[[0, 80, 600, 80, 600, 336, 0, 336]], segpx=0, segopt=0, od=1, conf=40, seg_param_type=0)
            seg_param = json.dumps(obj=[[0, 80, 600, 80, 600, 336, 0, 336]])
            # data = dict(seg=seg_param, segpx=0, segopt=0, od=1, conf=40, seg_param_type=1)
            # data = dict(segpx=0, segopt=0, od=1, conf=40)

            # type = 3 det + seg
            # r = requests.post(url, files=files, data=data)
            # type = 1 det
            time_start = time.time()

            r = requests.post(url, files=files, data=data)
            print(r.headers)
            result = json.loads(s=r.text)
            print(time.time() - time_start)
            print(result)
            print(r.text)
            # print(result['time_used'])
            # time_total_para += result['prepare_time']
            # time_total += result['time_used']
            # time_algo += result['algo_time']
            # time_db += result['time_db']
            # image_time += result['image_time']
            # infer_time += result['infer_time']

            # if i == (circle_num-1):
            #     detail_time = result['detail_time']
        # singal_ssd_time += result['ssd_inference']
        # pose_time_total += result['pose_time']
        # reid_time_total += result['reid_time']
        # work_time += result['work_time']
        # image_time += result['image_time']
        # infer_time += result['infer_time']
        except Exception as e:
            print('***********')
            print(e)
            traceback.print_exc()
            print('***********')
            # print('response: ' + json.dumps(result))
            print('response: ' + r.text)
            with open('error_' + log, 'w') as w:
                w.write('response: ' + r.text + '\n')

    # client_mean_time = 'client mean time cost {:.4f} \n'.format(time_algo / circle_num)
    # pre_time_cost = 'pre time cost {:.4f} \n'.format(time_total_para / circle_num)
    # db_time_cost = 'db time cost {:.4f} \n'.format(time_db / circle_num)
    # total_time = 'total time used cost {:.4f} \n'.format(time_total / circle_num)
    # post_mean_time = 'post mean time cost {:.4f} \n'.format((time.time() - time_begin) / circle_num)
    # image_mean_time = 'image io time cost {:.4f} \n'.format(image_time/circle_num)
    # infer_mean_time = 'infer time cost {:.4f} \n'.format(infer_time/circle_num)
    #
    # # print('work time cost {:.4f}'.format(work_time/circle_num))
    # print('image io time cost {:.4f}'.format(image_time/circle_num))
    # print('infer time cost {:.4f}'.format(infer_time/circle_num))
    # #
    # # print('ssd mean time cost {:.4f}'.format(singal_ssd_time/circle_num))
    # # print('pose mean time cost {:.4f}'.format(pose_time_total/circle_num))
    # # print('reid mean time cost {:.4f}'.format(reid_time_total/circle_num))
    # print('client mean time cost {:.4f}'.format(time_algo / circle_num))
    # print('pre time cost {:.4f}'.format(time_total_para / circle_num))
    # print('db time cost {:.4f}'.format(time_db / circle_num))
    # print('total time used cost {:.4f}'.format(time_total / circle_num))
    # print('post mean time cost {:.4f}'.format((time.time() - time_begin) / circle_num))
    # with open(log, 'w') as w:
        # w.write(image_mean_time)
        # w.write(infer_mean_time)
        # w.write(client_mean_time)
        # w.write(pre_time_cost)
        # w.write(db_time_cost)
        # w.write(total_time)
        # w.write(post_mean_time)
        # w.write(json.dumps(detail_time))
        # w.write('response: ')
        # w.write(r.text + '\n')



if __name__ == '__main__':
    gpu_id = sys.argv[1]
    log = 'uploadPic_{}.log'.format(gpu_id)
    uploadFile(log)
