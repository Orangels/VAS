from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
from flask_cors import CORS
import time
import os
import json
from werkzeug.routing import BaseConverter
import random
import traceback
import uuid
from gearman_client import *

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 返回中文 不乱码
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # 保存文件位置
app.url_map.converters['regex'] = RegexConverter


CORS(app, resources=r'/*')


def random_filename(file):
    file_name, extension_name = os.path.splitext(file)
    random_name = uuid.uuid4().hex
    # random_name = str(random.randint(1, 10000))
    return file_name + '_' + random_name + extension_name


@app.route('/api/v1/detect', methods=['POST'])
def detect_det_seg():
    try:
        '''
            获取参数
        '''
        time_start = time.time()
        # 0: list,  1:str
        seg_param_test_type = int(request.values.get('seg_param_type', 1))
        if seg_param_test_type:
            seg_param = eval(request.values.get('seg', '[]'))
        else:
            seg_param = request.values.getlist('seg')
        # seg_param = request.values.getlist('seg')
        # seg_param = eval(request.values.get('seg'))
        seg_param_points = []
        for i, item in enumerate(seg_param):
            if seg_param_test_type == 0:
                seg_param[i] = list(eval(item))
            seg_param_points.append([])
            for j in range(0, len(seg_param[i]), 2):
                seg_param_points[i].append((seg_param[i][j], seg_param[i][j+1]))
        seg_type = len(seg_param)
        od = int(request.values.get('od', 1))
        # 是否返回语义分割结果-像素点坐标数组，0 or 1, 缺省为0 只在seg参数指定时有效
        segpx = int(request.values.get('segpx', 0))

        # 语义分割结果选项，0: 返回覆盖部分(占比/像素), 1: 返回裸露部分。缺省为 0, -1 为自定义无参数
        segopt = int(request.values.get('segopt', 0))
        conf = int(request.values.get('conf', 0))
        detect_type = 1
        if od == 1 and seg_type == 0:
            detect_type = 1
        elif od == 0 and seg_type != 0:
            detect_type = 2
        elif od == 1 and seg_type != 0:
            detect_type = 3
        elif od == 0 and seg_type == 0:
            dic = dict(code=400, result={
                'objs': [],
                'segs': [],
            })
            return jsonify(dic)


        '''
           获取上传图片
        '''
        uploaded_file = request.files['img']
        name = uploaded_file.filename
        year = time.strftime('%Y', time.localtime())
        month = time.strftime('%m', time.localtime())
        day = time.strftime('%d', time.localtime())
        ip = request.remote_addr

        # 日期地址
        date_path = year + '/' + month + '/' + day + '/'
        file_dir_path = BASE_DIR + '/' + app.config['UPLOAD_FOLDER'] + ip + '/' + date_path
        if not os.path.exists(file_dir_path):
            os.makedirs(file_dir_path)
        random_name = random_filename(name)
        # random_name = name
        filePs = file_dir_path + random_name
        uploaded_file.save(filePs)
        time_gearman_start = time.time()
        print('gearman start')
        gearman_res = client(detect_type, filePs, seg_param_points, segpx, segopt, conf)
        print('gearman end')
        print('gearman cost {}'.format(time.time()-time_gearman_start))
        os.remove(filePs)
        print('api cost {}'.format(time.time() - time_start))
        dic = dict(code=200, result=gearman_res)
        return jsonify(dic)
    except Exception as e:
        print('***********')
        print(e)
        traceback.print_exc()
        print('***********')
        dic = dict(code=400, result={
            'objs': [],
            'segs': [],
        })
        return jsonify(dic)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)