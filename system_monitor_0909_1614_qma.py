# 代码生成时间: 2025-09-09 16:14:26
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple system performance monitor tool using Python and Bottle framework.
"""

import os
import psutil
import bottle

# Define the route for system performance
@bottle.route("/performance")
def get_performance():
    """
    Returns system performance metrics as JSON response.
    """
    try:
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        network_io = psutil.net_io_counters()
        
        # Prepare the response data
        response = {
            "cpu_usage": cpu_usage,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "free": memory.free,
                "percent": memory.percent
            },
            "disk_usage": {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": disk_usage.percent
            },
            "network_io": {
                "bytes_sent": network_io.bytes_sent,
                