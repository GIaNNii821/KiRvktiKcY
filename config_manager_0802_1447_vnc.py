# 代码生成时间: 2025-08-02 14:47:14
from bottle import Bottle, run, route, static_file, request, response, template
import json
import os

# 定义配置文件管理器应用
app = Bottle()

# 配置文件路径
CONFIG_DIR = './configs/'

# 确保配置目录存在
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# 获取配置文件列表的路由
@route('/configs')
def list_configs():
    """
    返回配置文件列表
    """
    try:
        config_files = [f for f in os.listdir(CONFIG_DIR) if os.path.isfile(os.path.join(CONFIG_DIR, f))]
        return json.dumps(config_files)
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# 获取单个配置文件的路由
@route('/configs/<config_name:path>')
def get_config(config_name):
    """
    根据文件名返回配置文件内容
    """
    try:
        config_path = os.path.join(CONFIG_DIR, config_name)
        with open(config_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        response.status = 404
        return json.dumps({'error': 'Config file not found'})
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# 创建或更新配置文件的路由
@route('/configs/<config_name:path>', method='POST')
def set_config(config_name):
    """
    创建或更新配置文件
    """
    try:
        config_path = os.path.join(CONFIG_DIR, config_name)
        with open(config_path, 'w') as f:
            f.write(request.body.read().decode('utf-8'))
        return {'status': 'success'}
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# 删除配置文件的路由
@route('/configs/<config_name:path>', method='DELETE')
def delete_config(config_name):
    """
    删除配置文件
    """
    try:
        config_path = os.path.join(CONFIG_DIR, config_name)
        os.remove(config_path)
        return {'status': 'success'}
    except FileNotFoundError:
        response.status = 404
        return json.dumps({'error': 'Config file not found'})
    except Exception as e:
        response.status = 500
        return json.dumps({'error': str(e)})

# 运行应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)