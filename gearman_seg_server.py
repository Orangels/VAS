import gearman
import cv2
import json
import sys
import time
import gearman
import traceback

gm_worker = gearman.GearmanWorker(['localhost:4730'])


def task_listener_reverse(gearman_worker, gearman_job):
    data_dict = json.loads(s=gearman_job.data)
    path = data_dict['path']
    seg_param = data_dict['seg_param']
    print(path)
    return json.dumps(obj={'smart_site_seg': {
        'path': path,
        'seg_param': seg_param
    }})


if __name__ == '__main__':
    # global POSE_EST
    # global GPU_ID
    if len(sys.argv) < 2:
        pass
    else:
        channel_id = int(sys.argv[1])
        pass
    gm_worker.set_client_id('python-worker')
    gm_worker.register_task('smart_site_seg', task_listener_reverse)
    gm_worker.work()