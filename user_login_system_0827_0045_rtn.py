# 代码生成时间: 2025-08-27 00:45:50
# 导入Bottle框架
from bottle import route, run, request, response, redirect
from bottle.ext import sqlalchemy
import hashlib
import os

# 配置数据库连接
DATABASE_URI = 'sqlite:///users.db'

# 初始化数据库，并定义用户模型
def init_db():
    db = sqlalchemy.Database(DATABASE_URI)
    db.create_all()

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True)
        password_hash = db.Column(db.String(128))

        # 验证密码是否正确
        def check_password(self, password):
            return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    return db, User

# 初始化数据库
db, User = init_db()

# 登录路由
@route('/login', method='GET')
def login():
    # 显示登录表单
    return """<form action="/login" method="post">
    Username: <input type="text" name="username"/>
    Password: <input type="password" name="password"/>
    <input type="submit" value="Login"/>
</form>"""

# 登录验证路由
@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # 查找用户
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # 登录成功
        response.set_cookie('username', username)
        redirect('/')
    else:
        # 登录失败
        return "Invalid username or password"

# 主页路由
@route('/')
def home():
    username = request.get_cookie('username', secret='my_secret_key')
    if username:
        return f"Hello, {username}!"
    else:
        redirect('/login')

# 注册新用户
@route('/register', method='POST')
def register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return "Username already exists"
    
    # 创建新用户
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return "User registered successfully"

# 启动服务器
if __name__ == '__main__':
    run(host='localhost', port=8080)