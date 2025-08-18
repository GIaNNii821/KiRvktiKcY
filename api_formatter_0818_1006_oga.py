# 代码生成时间: 2025-08-18 10:06:23
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API Response Formatter

This script is designed to format API responses using the Bottle framework.
It provides a simple and easy-to-use interface for formatting responses.
"""

from bottle import Bottle, response, HTTPResponse
import json

# Create an instance of the Bottle application
app = Bottle()

# Define a default response formatter
def default_response_formatter(data, message, status_code=200, headers=None):
    if headers is None:
        headers = {}
    response.status = status_code
    response.content_type = 'application/json'
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Cache-Control', 'no-cache')
    return json.dumps({
        'status': 'success' if status_code < 400 else 'error',
        'message': message,
        'data': data
    }, ensure_ascii=False)

# Define an error response formatter
def error_response_formatter(message, status_code=400):
    response.status = status_code
    response.content_type = 'application/json'
    return json.dumps({
        'status': 'error',
        'message': message,
        'data': {}
    }, ensure_ascii=False)

# Define a route to test the API response formatting
@app.route('/format', method='GET')
def format_api_response():
    try:
        # Simulate some data to be returned by the API
        data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        }
        return default_response_formatter(data, 'Data retrieved successfully')
    except Exception as e:
        # Handle any unexpected errors and return an error response
        return error_response_formatter(str(e))

# Run the Bottle application
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
