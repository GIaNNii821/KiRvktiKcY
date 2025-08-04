# 代码生成时间: 2025-08-04 14:27:40
# theme_switcher.py
# This Bottle app allows you to toggle between two themes: 'light' and 'dark'.

from bottle import Bottle, request, response, route, run, template

# Create a Bottle instance
app = Bottle()

# Define the theme cookies
COOKIE_NAME = 'theme'
COOKIES = {'light': 'light', 'dark': 'dark'}

# Route to set the theme
@route('/set_theme/<theme_name>')
def set_theme(theme_name):
    # Check if the theme is valid
    if theme_name in COOKIES:
        # Set the response cookie
        response.set_cookie(COOKIE_NAME, COOKIES[theme_name], max_age=31536000)  # one year
        return f'Theme set to {theme_name}'
    else:
        # Return an error if the theme is not valid
        return 'Invalid theme', 400

# Route to get the current theme
@route('/get_theme')
def get_theme():
    # Get the theme from the cookie, default to 'light' if not set
    theme = request.get_cookie(COOKIE_NAME, 'light')
    return f'Current theme is {theme}'

# Route to switch the theme. It toggles between 'light' and 'dark'
@route('/switch_theme')
def switch_theme():
    # Get the current theme from the cookie
    current_theme = request.get_cookie(COOKIE_NAME, 'light')
    # Switch to the next theme
    if current_theme == COOKIES['light']:
        new_theme = COOKIES['dark']
    else:
        new_theme = COOKIES['light']
    # Set the new theme in the response cookie
    response.set_cookie(COOKIE_NAME, new_theme, max_age=31536000)  # one year
    return f'Theme switched to {new_theme}'

# Define the 'root' page route
@route('/')
def index():
    # Get the current theme to show the appropriate template
    theme = request.get_cookie(COOKIE_NAME, 'light')
    # Render the template with the current theme
    return template('index', theme=theme)

# Run the Bottle application on localhost at port 8080
run(app, host='localhost', port=8080)

# Template for the 'index' page
TEMPLATES = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Theme Switcher</title>
</head>
<body>
    <h1>Theme Switcher</h1>
    <p>Welcome to the theme switcher application.</p>
    <p><a href="/switch_theme">Switch Theme</a></p>
    <p>Current theme: {{theme}}</p>
</body>
</html>
"""