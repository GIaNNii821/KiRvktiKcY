# 代码生成时间: 2025-08-14 08:44:28
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple system performance monitor using the Bottle framework.
"""

from bottle import route, run, template, request
import psutil
import json
import datetime

# Define the base URL for the application
BASE_URL = '/monitor'

# Create a Bottle WSGI application
app = application = Bottle()


@route("/" + BASE_URL)
def monitor():
    """
    Handles GET requests to the base URL and returns system performance data.
    """
    try:
        # Collect system performance metrics
        system_info = {}
        system_info['cpu_usage'] = psutil.cpu_percent(interval=1)
        system_info['memory_usage'] = psutil.virtual_memory().percent
        system_info['disk_usage'] = psutil.disk_usage('/').percent
        system_info['timestamp'] = datetime.datetime.now().isoformat()

        # Return the system performance data in JSON format
        return json.dumps(system_info)
    
    except Exception as e:
        # Handle any exceptions that occur during data collection
        return json.dumps({'error': str(e)})


# Run the Bottle application on port 8080
run(app, host='localhost', port=8080, debug=True)
