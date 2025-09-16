# 代码生成时间: 2025-09-17 00:47:33
# 数据模型应用
# 使用Bottle框架实现

# 导入Bottle和相关模块
from bottle import route, run, request, response, static_file
from bottle.ext import sqlite
import json

# 配置数据库
DATABASE = 'data_model.db'

# 定义数据模型类
class DataModel:
    def __init__(self, db):
        self.db = db

    # 创建表
    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        self.db.execute(sql)

    # 添加用户
    def add_user(self, user_name, user_age):
        sql = "INSERT INTO users (name, age) VALUES (?, ?)"
        self.db.execute(sql, (user_name, user_age))
        self.db.commit()

    # 获取所有用户
    def get_users(self):
        sql = "SELECT * FROM users"
        result = self.db.execute(sql)
        users = [dict(id=row[0], name=row[1], age=row[2]) for row in result]
        return users

    # 更新用户
    def update_user(self, user_id, user_name, user_age):
        sql = "UPDATE users SET name=?, age=? WHERE id=?"
        self.db.execute(sql, (user_name, user_age, user_id))
        self.db.commit()

    # 删除用户
    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id=?"
        self.db.execute(sql, (user_id,))
        self.db.commit()

# 创建Bottle应用
app = application = sqlite.BottleSqlite(DATABASE)

# 初始化数据库
@app.route('/init-db', method='GET')
def init_db():
    data_model = DataModel(app.db)
    data_model.create_table()
    return {"message": "Database initialized"}

# 添加用户
@app.route('/add-user', method='POST')
def add_user():
    try:
        name = request.json.get("name")
        age = request.json.get("age")
        if not name or not age:
            response.status = 400
            return {"error": "Missing name or age"}
        data_model = DataModel(app.db)
        data_model.add_user(name, age)
        return {"message": "User added"}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

# 获取所有用户
@app.route('/users', method='GET')
def get_users():
    data_model = DataModel(app.db)
    users = data_model.get_users()
    return {"users": users}

# 更新用户
@app.route('/update-user/<user_id:int>', method='PUT')
def update_user(user_id):
    try:
        name = request.json.get("name")
        age = request.json.get("age")
        if not name or not age:
            response.status = 400
            return {"error": "Missing name or age"}
        data_model = DataModel(app.db)
        data_model.update_user(user_id, name, age)
        return {"message": "User updated"}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

# 删除用户
@app.route('/delete-user/<user_id:int>', method='DELETE')
def delete_user(user_id):
    try:
        data_model = DataModel(app.db)
        data_model.delete_user(user_id)
        return {"message": "User deleted"}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

# 运行应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080)