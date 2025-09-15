# 代码生成时间: 2025-09-16 04:43:30
#!/usr/bin/env python

"""
A simple system performance monitoring tool using the Bottle framework.
"""

from bottle import route, run, template, request
import psutil
import json
import os

# Define the base URL for the application
BASE_URL = 'http://localhost:8080'

# Define the maximum number of CPUs to display in the CPU usage chart
MAX_CPU_USAGE_DISPLAY = 10

# Get system uptime
def get_system_uptime():
    """Returns the system uptime in seconds."""
    return psutil.boot_time()

# Get CPU usage
def get_cpu_usage():
    """Returns a list of CPU usage percentages."""
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

# Get memory usage
def get_memory_usage():
    """Returns a dictionary containing memory usage data."""
    memory = psutil.virtual_memory()
    return {
        'available': memory.available,
        'used': memory.used,
        'percent': memory.percent
    }

# Get disk usage
def get_disk_usage():
    """Returns a dictionary containing disk usage data for all partitions."""
    disk_usage = {}
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage[partition.device] = {
            'total': usage.total,
            'used': usage.used,
            'percent': usage.percent,
            'mountpoint': partition.mountpoint
        }
    return disk_usage

# Bottle route for system uptime endpoint
@route('/uptime')
def uptime():
    """Returns the system uptime in JSON format."""
    try:
        uptime_seconds = get_system_uptime()
        return json.dumps({'uptime': uptime_seconds})
    except Exception as e:
        return json.dumps({'error': str(e)})

# Bottle route for CPU usage endpoint
@route('/cpu_usage')
def cpu_usage():
    """Returns a list of CPU usage percentages in JSON format."""
    try:
        cpu_percentages = get_cpu_usage()
        return json.dumps({'cpu_usage': cpu_percentages})
    except Exception as e:
        return json.dumps({'error': str(e)})

# Bottle route for memory usage endpoint
@route('/memory_usage')
def memory_usage():
    """Returns memory usage data in JSON format."""
    try:
        memory_data = get_memory_usage()
        return json.dumps({'memory_usage': memory_data})
    except Exception as e:
        return json.dumps({'error': str(e)})

# Bottle route for disk usage endpoint
@route('/disk_usage')
def disk_usage():
    """Returns disk usage data for all partitions in JSON format."""
    try:
        disk_data = get_disk_usage()
        return json.dumps({'disk_usage': disk_data})
    except Exception as e:
        return json.dumps({'error': str(e)})

# Run the Bottle server
if __name__ == '__main__':
    run(host='localhost', port=8080)
