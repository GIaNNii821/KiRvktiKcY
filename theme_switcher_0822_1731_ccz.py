# 代码生成时间: 2025-08-22 17:31:04
from bottle import route, run, request, response, template

# 定义主题选项
THEMES = {
    'light': 'Light Blue',
    'dark': 'Dark Blue',
}

# 存储当前主题的全局变量
current_theme = 'light'

# 路由：主题切换
@route('/switch_theme/<theme_name>')
def switch_theme(theme_name):
    # 错误处理：确保主题名称有效
    if theme_name not in THEMES:
        response.status = 404
        return template('error', error='Invalid theme name')
    
    # 更新全局变量中的当前主题
    global current_theme
    current_theme = theme_name
    return template('theme_switched', theme=current_theme)

# 主页路由：显示当前主题
@route('/')
def home():
    return template('home', theme=current_theme)

# 启动服务器
if __name__ == '__main__':
    run(host='localhost', port=8080)

# 模板：主页，显示当前主题
home_template = """
<html>
<head><title>Theme Switcher</title></head>
<body>
    <h1>Welcome to the Theme Switcher</h1>
    <p>Your current theme is: {{theme}}</p>
    <a href="/switch_theme/light">Switch to Light Theme</a>
    <a href="/switch_theme/dark">Switch to Dark Theme</a>
</body>
</html>
"""

# 模板：主题切换成功
theme_switched_template = """
<html>
<head><title>Theme Switched</title></head>
<body>
    <h1>Theme Switched</h1>
    <p>Your theme has been switched to: {{theme}}</p>
    <a href="/">Go Home</a>
</body>
</html>
"""
# 模板：错误页面
error_template = """
<html>
<head><title>Error</title></head>
<body>
    <h1>Error</h1>
    <p>{{error}}</p>
</body>
</html>
"""