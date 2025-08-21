# 代码生成时间: 2025-08-21 19:59:36
from bottle import route, run, request, response, redirect
from functools import wraps

# Define a simple in-memory user database for demonstration purposes.
# In a real-world application, this would be replaced with a database.
USER_DATABASE = {
    "admin": "password123"
}

# Define a decorator to handle user authentication.
def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if the user is authenticated.
        if not request.get_cookie("authenticated"):
            redirect("/login")  # Redirect to login page if not authenticated.
        return f(*args, **kwargs)
    return wrapper


# Define a login route.
@route("/login", method="GET")
def login():
    """
    Show the login page.
    """
    return "<form action='/login' method='post'>Username: <input type='text' name='username'><br>Password: <input type='password' name='password'><br><input type='submit' value='Login'></form>"


@route("/login", method="POST")
def do_login():
    """
    Handle user login.
    """
    username = request.forms.get("username")
    password = request.forms.get("password")
    if USER_DATABASE.get(username) == password:
        response.set_cookie("authenticated", "yes")
        redirect("/dashboard")
    else:
        return "Invalid username or password."


@route("/dashboard")
@auth_required
def dashboard():
    """
    Show the dashboard page.
    """
    return "Welcome to the dashboard, you are now authenticated."


@route("/logout")
def logout():
    """
    Handle user logout.
    """
    response.delete_cookie("authenticated")
    redirect("/login")


# Run the Bottle application.
run(host='localhost', port=8080)
