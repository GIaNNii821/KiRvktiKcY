# 代码生成时间: 2025-08-31 02:33:02
# folder_organizer.py
# This script uses the Bottle framework to create a web application
# that organizes folders based on specified rules.

from bottle import route, run, request, template
import os
import shutil

# Define the root directory where the script will operate
ROOT_DIR = "./"

# Organize function to move files into their respective folders
def organize_files(directory):
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                # Determine file categorization (e.g., by extension)
                _, ext = os.path.splitext(item)
                if ext:
                    target_folder = os.path.join(directory, ext[1:])
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    shutil.move(item_path, target_folder)
    except Exception as e:
        return f"An error occurred: {e}"

# Bottle route to handle the organization of a folder
@route('/organize', method='POST')
def organize():
    # Get the directory path from the request form
    dir_path = request.forms.get('directory')
    
    # Check if the directory path is provided
    if not dir_path:
        return template("Error: No directory path provided.")
    
    # Check if the directory exists
    if not os.path.exists(dir_path):
        return template("Error: Directory does not exist.")
    
    # Organize the files in the directory
    result = organize_files(dir_path)
    
    # Return the result or an error message
    return template(f"Result: {result}")

# Bottle route serving the web form to input directory path
@route('/')
def index():
    return template("""
    <html><body>
    <form action="/organize" method="post">
    Directory path: <input type="text" name="directory"><br>
    <input type="submit" value="Organize">
    </form>
    </body></html>
    """)

# Start the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080)
