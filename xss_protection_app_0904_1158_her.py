# 代码生成时间: 2025-09-04 11:58:35
#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
A simple Bottle web application with basic XSS protection.
"""
import bottle
from markupsafe import escape

# Define a route and a corresponding callback function
# to handle all requests to the application
@bottle.route('/')
def index():
    # Escape user input to prevent XSS attacks
    return "Hello, <b>World</b>!"

@bottle.route('/xss', method='GET')
def xss_test():
    # This function intentionally demonstrates a vulnerability
    # and should be replaced with proper input sanitization.
    # For demonstration purposes only.
    user_input = bottle.request.query.get('input')
    # In a real-world application, you should never directly
    # insert user input into the HTML without proper escaping.
    return f"User Input: {user_input}"

@bottle.route('/safe', method='GET')
def safe_xss_test():
    # This function demonstrates how to properly handle user input
    user_input = bottle.request.query.get('input')
    # Use escape() function from markupsafe to prevent XSS attacks
    safe_input = escape(user_input)
    return f"Safe User Input: {safe_input}"

# Error handler for 404 errors
@bottle.error(404)
def error_404(error):
    '''
    Custom error handler for 404 errors.
    Returns a simple error message to the client.
    '''
    return "Error 404: The resource could not be found."

# Run the Bottle application
if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)
