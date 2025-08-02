# 代码生成时间: 2025-08-02 08:09:46
#!/usr/bin/env python

"""
定时任务调度器，使用Bottle框架实现。
支持定时任务的添加、删除、执行和查看状态。
"""

import bottle
from bottle.ext import jinja2
from datetime import datetime, timedelta
import schedule
import threading
import time

# 定时任务存储
tasks = {}

# 添加任务
def add_task(name, interval, func):
    tasks[name] = {'interval': interval, 'func': func}

# 移除任务
def remove_task(name):
    if name in tasks:
        del tasks[name]

# 执行任务
def run_task(name):
    if name in tasks:
        tasks[name]['func']()

# 定时任务调度器
def scheduler():
    while True:
        for name, task in tasks.items():
            run_task(name)
        schedule.run_pending()
        time.sleep(task['interval'])

# 启动调度器
def start_scheduler():
    threading.Thread(target=scheduler).start()

# 定时任务执行函数示例
def example_task():
    print(f"Task executed at {datetime.now()}")

# Bottle视图函数
@bottle.route("/")
def index():
    return "Welcome to the task scheduler!"

@bottle.route("/add", method="POST\)
def add():
    try:
        name = bottle.request.forms.get("name")
        interval = bottle.request.forms.get("interval\)
        add_task(name, int(interval), example_task)
        return f"Task {name} added successfully."
    except Exception as e:
        return f"Error: {str(e)}"

@bottle.route("/remove", method="POST\)
def remove():
    try:
        name = bottle.request.forms.get("name")
        remove_task(name)
        return f"Task {name} removed successfully."
    except Exception as e:
        return f"Error: {str(e)}"

@bottle.route("/run", method="POST\)
def run():
    try:
        name = bottle.request.forms.get("name\)
        run_task(name)
        return f"Task {name} executed."
    except Exception as e:
        return f"Error: {str(e)}"

@bottle.route("/status")
def status():
    return str(tasks)

# 启动Bottle应用
if __name__ == "__main__":
    start_scheduler()
    bottle.run(host="localhost", port=8080, debug=True)
