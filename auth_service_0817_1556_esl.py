# 代码生成时间: 2025-08-17 15:56:30
from bottle import route, run, request, response

# 模拟数据库，存储用户信息
USER_DATABASE = {
    "admin": {"username": "admin", "password": "adminpass"}
}

# 用户认证函数
def authenticate_user(username, password):
    """
    验证用户名和密码是否匹配。
    
    :param username: 用户名
    :param password: 密码
    :return: 如果认证成功返回True，否则返回False
    """
    user_info = USER_DATABASE.get(username)
    if user_info and user_info['password'] == password:
        return True
    return False

# 设置认证装饰器
def require_auth(func):
    """
    检查用户是否已经认证。
    
    :param func: 被装饰的函数
    :return: 装饰后的函数
    """
    def wrapper(*args, **kwargs):
        auth_user = request.get_cookie('auth_user')
        if not auth_user or not authenticate_user(auth_user['username'], auth_user['password']):
            response.status = 401  # 未认证
            return {"error": "Unauthorized"}
        return func(*args, **kwargs)
    return wrapper

# 登录路由
@route('/login', method='POST')
def login():
    """
    处理用户登录，如果认证成功，设置认证cookie。
    """
    username = request.forms.get('username')
    password = request.forms.get('password')
    if authenticate_user(username, password):
        auth_user = {"username": username, "password": password}
        response.set_cookie('auth_user', str(auth_user), path='/')
        return {"message": "Login successful"}
    else:
        response.status = 401  # 认证失败
        return {"error": "Invalid username or password"}

# 用户信息路由
@route('/profile')
@require_auth
def profile():
    """
    展示用户信息。需要用户认证。
    """
    auth_user = eval(request.get_cookie('auth_user'))
    return {"username": auth_user['username'], "message": "Welcome to your profile"}

# 运行服务
if __name__ == '__main__':
    run(host='localhost', port=8080)