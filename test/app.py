from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
from flask_cors import CORS
import time
import os
import json
from werkzeug.routing import BaseConverter
import random
import traceback
import uuid


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


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

        seg_param = request.values.getlist('seg[]')
        for i, item in enumerate(seg_param):
            seg_param[i] = list(eval(item))

        dic = dict(Results=200, Cause='OK')
        return jsonify(dic)
    except Exception as e:
        print('***********')
        print(e)
        traceback.print_exc()
        print('***********')
        dic = dict(Results=400, result={
            'objs': [],
            'segs': [],
        })
        return jsonify(dic)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)