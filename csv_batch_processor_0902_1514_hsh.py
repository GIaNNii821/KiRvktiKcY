# 代码生成时间: 2025-09-02 15:14:27
import bottle
import csv
import os
from bottle import request, response, static_file
from io import StringIO

# 设置静态文件目录
STATIC_FOLDER = 'static'

# 定义全局变量
ALLOWED_EXTENSIONS = {'csv'}

"""
检查文件扩展名是否被允许
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
处理上传的CSV文件"""

def process_csv_file(file):
    # 将文件内容读入StringIO对象
    file_content = StringIO(file.file.read().decode('utf-8'))
    csv_file = csv.reader(file_content)
    processed_data = []
    try:
        for row in csv_file:
            processed_data.append(row)
    except csv.Error as e:
        # 处理CSV解析错误
        return {'error': f'CSV parsing error: {e}'}, 400
    return processed_data

"""
Bottle路由：上传CSV文件"""
@bottle.route('/upload', method='POST')
@bottle.view('upload')
def upload():
    if request.files.get('file'):
        file = request.files['file']
        if allowed_file(file.filename):
            # 处理CSV文件
            result = process_csv_file(file)
            if 'error' in result:
                return result
            else:
                # 返回处理结果
                return {'data': result}
        else:
            return {'error': 'Invalid file extension. Only CSV files are allowed.'}, 400
    return {'error': 'No file part'}, 400

"""
Bottle路由：静态文件服务
"""
@bottle.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_FOLDER)

"""
Bottle路由：主页
"""
@bottle.route('/')
def index():
    return static_file('index.html', root=STATIC_FOLDER)

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)