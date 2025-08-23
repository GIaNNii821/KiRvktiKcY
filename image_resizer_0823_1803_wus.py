# 代码生成时间: 2025-08-23 18:03:40
from bottle import route, run, request, response
from PIL import Image
import os
# 改进用户体验

# 配置文件存储路径
UPLOAD_FOLDER = './uploads/'
OUTPUT_FOLDER = './output/'

# 确保上传和输出文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
# 扩展功能模块
    os.makedirs(OUTPUT_FOLDER)

# 批量调整图片尺寸的路由
@route('/upload', method='POST')
def upload_file():
# TODO: 优化性能
    try:
        # 检查是否有文件在请求中
        files = request.files
        if not files:
            return {'error': 'No files found'}

        # 遍历上传的文件
        for file in files.values():
            # 保存文件到上传文件夹
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

            # 尝试打开并调整图片尺寸
            with Image.open(os.path.join(UPLOAD_FOLDER, file.filename)) as img:
                width, height = 800, 600  # 目标尺寸
                img = img.resize((width, height), Image.ANTIALIAS)

                # 保存调整后的图片到输出文件夹
                filename_without_ext = os.path.splitext(file.filename)[0]
                output_filename = f"{filename_without_ext}_resized.jpg"
                img.save(os.path.join(OUTPUT_FOLDER, output_filename))

        return {'message': 'Files processed successfully'}
    except Exception as e:
        return {'error': str(e)}

# 设置静态文件服务路由
@route('/output/<filename:path>')
def serve_file(filename):
    return static_file(filename, root=OUTPUT_FOLDER)
# 改进用户体验

# 启动Bottle服务
if __name__ == '__main__':
    run(host='localhost', port=8080)
