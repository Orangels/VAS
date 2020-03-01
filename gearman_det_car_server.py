import gearman
import cv2
import json
import sys
import time
import gearman
import traceback

sys.path.append('/home/user/workspace/priv-0220/Pet-engine')
sys.path.append('/home/user/workspace/priv-0220/Pet-dev')
from modules import pet_engine

threshold_default = 0.7
det = None
labels = ['背景', '推土机', '挖掘机', '压路机']

oid = dict(推土机=4, 挖掘机=1, 压路机=9)

gm_worker = gearman.GearmanWorker(['localhost:4730'])


def task_listener_reverse(gearman_worker, gearman_job):
    data_dict = json.loads(s=gearman_job.data)
    path = data_dict['path']
    # 传参临时阈值, 0 时为默认阈值, 百分比整数
    od_conf = int(data_dict['od_conf'])
    print(path)
    time_read_img_start = time.time()
    img = cv2.imread(path)
    time_read_img_end = time.time()
    # 4 * n * 5  类别, 个数, 坐标+置信度
    time_start = time.time()
    output = det(img)
    time_inference_end = time.time()
    print(output)
    print(len(output))
    result_arr = []
    for i, item in enumerate(output):
        if type(item) is not list:
            output[i] = item.tolist()
            print(output[i])
            for count_i, count_item in enumerate(output[i]):
                for coor_i, coor_item in enumerate(count_item):
                    if coor_i != 4 and coor_i != 5:
                        coor_item = int(coor_item)
                        output[i][count_i][coor_i] = coor_item
                        # output[i][count_i][coor_i] = int(output[i][count_i][coor_i])
                    elif coor_i == 4:
                        threshold_used = threshold_default
                        if od_conf != 0:
                            threshold_used = od_conf / 100
                        if coor_item > threshold_used:
                            coor_item = int(coor_item * 100)
                            output[i][count_i][coor_i] = coor_item
                            result_arr.append(dict(label=labels[i], box=count_item[:4], conf=coor_item,
                                                   oid=oid[labels[i]]))
                        # output[i][count_i][coor_i] = int(output[i][count_i][coor_i]*100)
                # img = cv2.rectangle(img, (count_item[0], count_item[1]), (count_item[2], count_item[3]), (0, 255, 0), 2)
    print(result_arr)
    print('read img cost time {}'.format(time_read_img_end-time_read_img_start))
    print('inference cost time {}'.format(time_inference_end-time_start))
    print('cost time {}'.format(time.time() - time_read_img_start))

    # with open('./logs/car_server.log', 'a+') as w:
    #     w.write('{}'.format(time.time() - time_start) + '\n')

    return json.dumps(obj={'smart_site_det_car': {
        'result': result_arr,
    }})


if __name__ == '__main__':
    # global POSE_EST
    # global GPU_ID

    module = pet_engine.MODULES['SSDDet']

    if len(sys.argv) < 2:
        det = module(cfg_file='./yaml/ssd_VGG16_512x512_1x_vehicle/ssd_VGG16_512x512_1x_vehicle_car.yaml',
                     cfg_list=['VIS.VIS_TH', threshold_default,
                               'VIS.SHOW_BOX.COLOR_SCHEME', None]
                     )
    else:
        channel_id = int(sys.argv[1])
        det = module(cfg_file='./yaml/ssd_VGG16_512x512_1x_vehicle/ssd_VGG16_512x512_1x_vehicle_car.yaml',
                     cfg_list=['VIS.VIS_TH', threshold_default,
                               'VIS.SHOW_BOX.COLOR_SCHEME', None,
                               'MODULES.SSDDET.GPU_ID', channel_id
                               ]
                     )
    gm_worker.set_client_id('python-worker')
    gm_worker.register_task('smart_site_det_car', task_listener_reverse)
    gm_worker.work()