# 代码生成时间: 2025-08-03 00:45:46
# system_monitor.py

# Import required libraries
# 增强安全性
from bottle import route, run, template
import psutil
import os
import sys

# Constants for configuration
HOST = 'localhost'
PORT = 8080

# Define the root route
@route('/')
def index():
    # Render the index template
    return template('index')

# Define the route for getting system information
@route('/info')
# 改进用户体验
def get_system_info():
    try:
        # Gather system information
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Create a dictionary to store the information
        info = {
            "cpu_usage": cpu_usage,
# 改进用户体验
            "memory_usage": memory_usage,
            "disk_usage": disk_usage
        }
        
        # Return the system information as JSON
        return {"status": "success", "data": info}
# 扩展功能模块
    except Exception as e:
        # Handle any exceptions that occur
        return {"status": "error", "message": str(e)}
# NOTE: 重要实现细节

# Define the route for getting system processes
@route('/processes')
def get_system_processes():
# NOTE: 重要实现细节
    try:
        # Get the list of processes
        processes = [p.info for p in psutil.process_iter(['pid', 'name', 'status', 'create_time'])]
# 扩展功能模块
        
        # Return the list of processes as JSON
        return {"status": "success", "data": processes}
    except Exception as e:
        # Handle any exceptions that occur
        return {"status": "error", "message": str(e)}

# Define the route for getting system network information
@route('/network')
def get_system_network_info():
    try:
        # Get network information
        network_io = psutil.net_io_counters()
        
        # Create a dictionary to store the information
        info = {
            "bytes_sent": network_io.bytes_sent,
            "bytes_recv": network_io.bytes_recv,
            "packets_sent": network_io.packets_sent,
            "packets_recv": network_io.packets_recv,
            "errin": network_io.errin,
            "errout": network_io.errout
        }
# 添加错误处理
        
        # Return the network information as JSON
        return {"status": "success", "data": info}
    except Exception as e:
        # Handle any exceptions that occur
        return {"status": "error", "message": str(e)}

# Route for returning system uptime
# FIXME: 处理边界情况
@route('/uptime')
def get_system_uptime():
# NOTE: 重要实现细节
    try:
        # Get system uptime
        uptime = psutil.boot_time()
        
        # Return the uptime as JSON
        return {"status": "success", "data": {
            "uptime": uptime
        }}
    except Exception as e:
        # Handle any exceptions that occur
        return {"status": "error", "message": str(e)}

# Start the Bottle server
if __name__ == '__main__':
    run(host=HOST, port=PORT)
