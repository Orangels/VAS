import gearman
import cv2
import json
import sys
import time
import gearman
import traceback
import torch
import numpy as np
from multiprocessing import Process, Queue, Pool, Manager
import os

from PIL import Image

from tool.utils import transform_extension_path

sys.path.append('/home/user/workspace/priv-0220/Pet-engine')
from core.semseg_priv_config import cfg_priv
sys.path.append(cfg_priv.PET_ROOT)
from modules import pet_engine

gm_worker = gearman.GearmanWorker(['localhost:4730'])
semseg_inference = None

q_file = Queue()
q_name = Queue()


def read_q(q_file, q_name):
    while True:
        if q_file.empty() and q_name.empty():
            file = q_file.get(True)
            name = q_name.get(True)
            print('name -- {}'.format(name))
            np.save(name, file)


def write_q(q_file, q_name):
    num = 0
    while True:
        if q_file.empty() and q_name.empty():
            q_file.put(num)
            q_name.put(num)
        num += 1
        time.sleep(1)


def task_listener_reverse(gearman_worker, gearman_job):
    global q_file
    global q_name
    time_start = time.time()
    data_dict = json.loads(s=gearman_job.data)
    path = data_dict['path']
    npy_path = transform_extension_path(path)
    seg_param = data_dict['seg_param']
    time_read_data = time.time()
    print('read time cost {}'.format(time_read_data - time_start))
    img_cv = cv2.imread(path)
    img_cv = img_cv[:, :, ::-1]
    time_read_img = time.time()
    print('read img time cost {}'.format(time_read_img-time_read_data))
    mask = semseg_inference(img_cv)
    time_inference = time.time()
    print('inference time cost {}'.format(time_inference-time_read_img))
    # print(path)
    # print(mask)
    # 多进程处理
    # q_file.put(mask)
    # q_name.put(npy_path)

    print('put queue value time cost {}'.format(time.time()-time_inference))
    # 单进程处理
    # print(npy_path)
    np.save(npy_path, mask)
    time_cost = time.time()-time_start
    print('api + read img cost {}'.format(time_cost))
    with open('./logs/det_server.log', 'a+') as w:
        w.write('{}'.format(time_cost) + '\n')
    return json.dumps(obj={'smart_site_seg': {
        'path': path,
        'seg_param': seg_param,
        'npy_path': npy_path
    }})


if __name__ == '__main__':
    # global POSE_EST
    # global GPU_ID
    module = pet_engine.MODULES['Semantc_Segmentation']
    if len(sys.argv) < 2:
        torch.cuda.set_device(0)
    else:
        channel_id = int(sys.argv[1])
        torch.cuda.set_device(channel_id)
    semseg_inference = module(cfg_file='/home/user/workspace/priv-0220/Vas/yaml/seg_smart_ground.yaml')
    
    # 启动 子进程
    # pr = Process(target=read_q, args=(q_file, q_name))
    # pr.start()

    # pw_1.join()
    # pr.join()
    
    gm_worker.set_client_id('python-worker')
    gm_worker.register_task('smart_site_seg', task_listener_reverse)
    gm_worker.work()