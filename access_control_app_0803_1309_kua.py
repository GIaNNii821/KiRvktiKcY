# 代码生成时间: 2025-08-03 13:09:15
#!/usr/bin/env python

"""
Simple Bottle application demonstrating access control.
"""

from bottle import route, run, request, response, abort
import functools

# Simulate a database of users
USERS = {
    "admin": "secret",
    "alice": "password123"
}

# Decorator for authentication
def check_auth(username, password):
    """Decorator to check if a given username and password are correct."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            auth = request.headers.get('Authorization')
            if auth:
                auth = auth.split(' ')
                if len(auth) == 2:
                    auth_username, auth_password = auth
                    if USERS.get(auth_username) == auth_password:
                        return func(*args, **kwargs)
            abort(401, 'Access denied.')
        return wrapper
    return decorator

# Define routes
@route('/')
def index():
    """Root route that is open to everyone."""
    return "Welcome to the access control demo."

@route('/admin')
@check_auth('admin', 'secret')
def admin_panel():
    """Admin panel route that requires authentication."""
    return "You are in the admin panel."

@route('/check-auth')
def check_authentication():
    """Route to check if authentication is set."""
    try:
        request.headers['Authorization']
        return "Authentication set."
    except KeyError:
        return "Authentication not set."

# Run the application
if __name__ == '__main__':
    run(host='localhost', port=8080)