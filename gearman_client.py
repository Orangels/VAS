import gearman
import json
from tool.utils import process_seg_result
import numpy as np
import os
import time


def check_request_status(job_request, detect_type, filePs=None, seg_param=[], segpx=0, segopt=-1):
    """
    :param job_request:
    :param detect_type: 1: detect, 2: seg 3: detect + seg
    :param seg_param: seg 检测区域
    :param segpx: 0: 不返回 seg 坐标, 1: 返回坐标
    :param segopt: -1 不返回覆盖比, 0: 覆盖部分覆盖比 1: 裸露部分覆盖比
    :return:
    """
    if detect_type == 1:
        gearman_res = {
            'objs': [],
            'segs': [],
        }
        for current_request in job_request:
            gearman_dic = json.loads(s=current_request.result, encoding='utf-8')
            print(gearman_dic)
            if 'smart_site_det_car' in gearman_dic:
                gearman_res['objs'] += gearman_dic['smart_site_det_car']['result']

            elif 'smart_site_det_fog' in gearman_dic:
                gearman_res['objs'] += gearman_dic['smart_site_det_fog']['result']
    elif detect_type == 2:
        gearman_dic = json.loads(s=job_request.result, encoding='utf-8')
        seg_result = process_seg_result(filePs=filePs, seg_param=seg_param, segpx=segpx, segopt=segopt,
                                        seg_mask=gearman_dic['smart_site_seg'])
        gearman_res = {
            'objs': [],
            'segs': seg_result,
        }
    elif detect_type == 3:
        gearman_res = {
            'objs': [],
            'segs': [],
        }
        for current_request in job_request:
            gearman_dic = json.loads(s=current_request.result, encoding='utf-8')
            print(gearman_dic)
            if 'smart_site_det_car' in gearman_dic:
                gearman_res['objs'] += gearman_dic['smart_site_det_car']['result']

            elif 'smart_site_det_fog' in gearman_dic:
                gearman_res['objs'] += gearman_dic['smart_site_det_fog']['result']
            else:
                seg_result = process_seg_result(filePs=filePs, seg_param=seg_param, segpx=segpx, segopt=segopt,
                                                seg_mask=gearman_dic['smart_site_seg'])
                gearman_res['segs'] = seg_result

    return gearman_res


def client(detect_type, filePs, seg_param, segpx=0, segopt=-1):
    """
    :param detect_type: 1: detect, 2: seg 3: detect + seg
    :param filePs:
    :param segpx: 0: 不返回 seg 坐标, 1: 返回坐标
    :param segopt: -1 不返回覆盖比, 0: 覆盖部分覆盖比 1: 裸露部分覆盖比
    :return:
    """
    gm_client = gearman.GearmanClient(['127.0.0.1:4730'])
    if detect_type == 1:
        print('type {}'.format(detect_type))
        jobs = [
            dict(task='smart_site_det_car', data=json.dumps(obj=dict(path=filePs))),
            dict(task='smart_site_det_fog', data=json.dumps(obj=dict(path=filePs)))
        ]
        completed_job_request = gm_client.submit_multiple_jobs(jobs, poll_timeout=60)
    elif detect_type == 2:
        print('type {}'.format(detect_type))
        completed_job_request = gm_client.submit_job("smart_site_seg", json.dumps(obj=dict(path=filePs,
                                                                                           seg_param=seg_param,
                                                                                           )))
    elif detect_type == 3:
        print('type {}'.format(detect_type))
        jobs = [
            dict(task='smart_site_det_car', data=json.dumps(obj=dict(path=filePs))),
            dict(task='smart_site_det_fog', data=json.dumps(obj=dict(path=filePs))),
            dict(task='smart_site_seg', data=json.dumps(obj=dict(path=filePs,
                                                        seg_param=seg_param,
                                                  )))
        ]
        completed_job_request = gm_client.submit_multiple_jobs(jobs, poll_timeout=60)
    return check_request_status(completed_job_request, detect_type, filePs=filePs, seg_param=seg_param, segpx=segpx,
                                segopt=segopt)


if __name__ == '__main__':
    time_start = time.time()
    img_path = '/home/user/workspace/priv-0220/privision_test/P000014.png'
    result = client(detect_type=2, filePs=img_path, seg_param=[[100, 200, 300, 400], [500, 600, 700, 800]], segpx=1,
                    segopt=0)
    print(result)
    print(os.path.exists(result))
    print(np.load(result))
    print(time.time()-time_start)
    # print(np.load('/home/user/workspace/priv-0220/privision_test/P000014.npy'))