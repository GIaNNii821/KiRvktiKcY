# 代码生成时间: 2025-08-12 17:48:52
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
定时任务调度器，使用Python和Bottle框架实现。
支持定时任务的添加、移除和执行。
"""

from bottle import Bottle, run, route, request
import threading
import time
from datetime import datetime
from threading import Thread

# 初始化Bottle应用
app = Bottle()

# 定时任务字典，存储任务及其执行时间
tasks = {}

# 添加定时任务
def add_task(name, interval, task_func):
    """
    添加一个定时任务。
    :param name: 任务名称
    :param interval: 执行间隔（秒）
    :param task_func: 任务函数
    """
    tasks[name] = {'interval': interval, 'task_func': task_func}
    print(f"任务 {name} 添加成功，间隔 {interval} 秒。")

# 移除定时任务
def remove_task(name):
    """
    移除一个定时任务。
    :param name: 任务名称
    """
    if name in tasks:
        del tasks[name]
        print(f"任务 {name} 移除成功。")
    else:
        print(f"任务 {name} 不存在。")

# 执行所有定时任务
def run_tasks():
    """
    执行所有定时任务。
    """
    while True:
        for name, task_info in tasks.items():
            # 获取任务函数和间隔时间
            task_func = task_info['task_func']
            interval = task_info['interval']
            # 打印任务执行信息
            print(f"任务 {name} 开始执行。时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            # 执行任务函数
            try:
                task_func()
            except Exception as e:
                print(f"任务 {name} 执行失败：{e}")
            # 等待间隔时间
            time.sleep(interval)

# 创建定时任务调度器线程
def start_scheduler():
    """
    启动定时任务调度器。
    """
    thread = Thread(target=run_tasks)
    thread.daemon = True  # 设置为守护线程
    thread.start()
    print("定时任务调度器启动成功。")

# Bottle路由：添加定时任务
@app.route('/add_task', method='POST')
def add_task_route():
    try:
        # 获取请求数据
        data = request.json
        name = data['name']
        interval = int(data['interval'])
        task_func = eval(data['task_func'])  # 动态执行任务函数
        # 添加定时任务
        add_task(name, interval, task_func)
        return {"status": "success", "message": f"任务 {name} 添加成功。"}
    except Exception as e:
        return {"status": "error", "message": f"添加任务失败：{e}"}

# Bottle路由：移除定时任务
@app.route('/remove_task', method='POST')
def remove_task_route():
    try:
        # 获取请求数据
        data = request.json
        name = data['name']
        # 移除定时任务
        remove_task(name)
        return {"status": "success", "message": f"任务 {name} 移除成功。"}
    except Exception as e:
        return {"status": "error", "message": f"移除任务失败：{e}"}

# Bottle路由：执行所有定时任务
@app.route('/run_tasks', method='POST')
def run_tasks_route():
    try:
        # 执行所有定时任务
        for name, task_info in tasks.items():
            task_func = task_info['task_func']
            task_func()
        return {"status": "success", "message": "所有任务执行成功。"}
    except Exception as e:
        return {"status": "error", "message": f