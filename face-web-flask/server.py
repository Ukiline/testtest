from matplotlib.font_manager import json_dump
from inference import Inference
from flask import Flask, request
from flask_cors import CORS
import base64
import numpy as np
from PIL import Image
import cv2
import json
import time

# base64编码转换为图片
def base64_to_image(base64_data, file_name):
    # base64编码转换为图片
    # 去掉base64编码头部
    print(base64_data)
    base64_data = base64_data[base64_data.find(',') + 1:]
    base64_data = base64_data.replace(' ', '+') # 替换空格
    base64_data = base64_data.encode('utf-8') # 解码
    base64_data = base64.b64decode(base64_data) # 解码
    # 解码内容转numpy数组
    img_array = np.fromstring(base64_data, np.uint8)
    img_np = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)
    with open(file_name, 'wb') as f:
        f.write(base64_data)
    return np.array(img_np)


#=================================Flask=======================================#
app = Flask(__name__)
# 解决跨域问题
CORS(app, resources=r'/*')

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/sketch', methods=['POST'])
def sketch():
    start_time = time.time()
    print(request.headers)
    # print(request.stream.read())
    # 获取body中的数据
    data = request.get_data()
    #print(data)
    # base64编码转换为图片
    # 获取时间戳
    date = time.time()
    sketch_raw = base64_to_image(str(data), './img/sketch' + str(date) +'.png')
    # 图片是白底黑字，需要转换为黑底白字
    sorted_Name = Inf.inference(255 - sketch_raw)
    # print(sorted_Name)
    response = json.dumps(sorted_Name)
    print('time:', time.time() - start_time)
    return response
    
if __name__ == '__main__':
    # 初始化模型
    Inf = Inference()
    print("Model Loaded")
    app.run(host='10.16.45.16', port=5000, debug=False)
#=================================Flask=======================================#
