# 代码生成时间: 2025-08-05 14:20:22
# 用户身份认证程序
# 使用Bottle框架
# FIXME: 处理边界情况

from bottle import route, run, request, response, redirect
# FIXME: 处理边界情况
from bottle.ext import sqlalchemy
import os
import hashlib

# 配置数据库连接
DATABASE_URI = 'sqlite:///users.db'

class User(db.Model):
    __tablename__ = 'users'
# NOTE: 重要实现细节
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
# 添加错误处理
        """将密码转换为散列值"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """检查密码是否匹配"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

# 初始化数据库模型
db.init(DATABASE_URI)
db.create_all()

# 用户登录路由
@route('/login', method='POST')
def login():
    """处理用户登录请求"""
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    if not username or not password:
        # 缺少用户名或密码
        return {'error': 'Missing username or password'}
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        # 用户不存在或密码错误
# 改进用户体验
        return {'error': 'Invalid username or password'}
    
    # 设置用户会话
    response.set_cookie('user_id', str(user.id))
    return {'message': 'Login successful'}

# 用户注册路由
@route('/register', method='POST')
def register():
    """处理用户注册请求"""
    username = request.forms.get('username')
    password = request.forms.get('password')
# FIXME: 处理边界情况
    
    if not username or not password:
        # 缺少用户名或密码
# 改进用户体验
        return {'error': 'Missing username or password'}
# 改进用户体验
    
    if User.query.filter_by(username=username).first():
        # 用户名已存在
# 扩展功能模块
        return {'error': 'Username already exists'}
# 改进用户体验
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return {'message': 'Registration successful'}

# 用户注销路由
@route('/logout')
def logout():
    """处理用户注销请求"""
    response.set_cookie('user_id', '', path='/', expires=0)
    return {'message': 'Logout successful'}

# 运行程序
if __name__ == '__main__':
    run(host='localhost', port=8080)
# NOTE: 重要实现细节