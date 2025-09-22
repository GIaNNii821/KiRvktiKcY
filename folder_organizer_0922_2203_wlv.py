# 代码生成时间: 2025-09-22 22:03:56
#!/usr/bin/env python

# folder_organizer.py
# This script organizes the contents of a specified directory by creating subdirectories
# and moving files into these subdirectories based on a specified pattern.

from bottle import route, run, request, response, static_file
import os
import shutil

# Define the root directory where the script will operate
ROOT_DIR = '/path/to/your/directory'

# Function to organize the files in the given directory
def organize_directory(path):
    try:
        # Check if the path is a directory
        if not os.path.isdir(path):
            raise ValueError(f"The path {path} is not a valid directory.")

        # Create subdirectories if they do not exist
        for category in ['documents', 'images', 'videos', 'others']:
            full_path = os.path.join(path, category)
            if not os.path.exists(full_path):
                os.makedirs(full_path)

        # Organize files
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                # Determine the category based on file extension
                if item.endswith(('.doc', '.docx', '.txt', '.pdf')):
                    destination = os.path.join(path, 'documents', item)
                elif item.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    destination = os.path.join(path, 'images', item)
                elif item.endswith(('.mp4', '.avi', '.mov')):
                    destination = os.path.join(path, 'videos', item)
                else:
                    destination = os.path.join(path, 'others', item)

                # Move the file to the appropriate directory
                shutil.move(item_path, destination)

        print("Files have been organized successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Bottle route to handle the file organization
@route('/organize', method='POST')
def organize_files():
    # Get the directory path from the POST request
    try:
        data = request.json
        directory_path = data.get('path')
        if not directory_path:
            raise ValueError('No directory path provided in the request.')

        # Organize the specified directory
        organize_directory(directory_path)
        response.status = 200
        return {'message': 'Directory organized successfully.'}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Set up the Bottle application to run on port 8080
run(host='localhost', port=8080, debug=True)
