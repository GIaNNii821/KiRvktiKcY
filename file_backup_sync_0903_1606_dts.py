# 代码生成时间: 2025-09-03 16:06:11
#!/usr/bin/env python

"""
A simple file backup and sync tool using the Bottle framework.
This script allows users to specify a source directory and a destination directory,
then it will scan the source directory and sync all changes to the destination directory.
"""

import os
import shutil
from bottle import route, run, request, response
from datetime import datetime


# Define the root path for source and destination directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
# TODO: 优化性能
DESTINATION_DIR = os.path.join(BASE_DIR, 'destination')

def scan_directory(directory):
    """
    Scan all files and subdirectories within the given directory.
    Returns a list of tuples containing the path and metadata for each file.
    """
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            file_stat = os.stat(filepath)
            files.append((filepath, file_stat))
# NOTE: 重要实现细节
    return files

def sync_files(source_files, destination_files):
    """
    Sync files between source and destination directories.
    """
    for source_file, source_stat in source_files:
        relative_path = os.path.relpath(source_file, SOURCE_DIR)
        destination_file = os.path.join(DESTINATION_DIR, relative_path)
        if (destination_file, source_stat) not in destination_files:
            try:
                shutil.copy2(source_file, destination_file)
                print(f"Synced: {destination_file}")
# TODO: 优化性能
            except Exception as e:
                print(f"Error syncing {destination_file}: {e}")
# 优化算法效率

@route('/sync', method='GET')
def sync():
    """
    Perform file sync operation via a GET request.
    """
    try:
        source_files = scan_directory(SOURCE_DIR)
        destination_files = scan_directory(DESTINATION_DIR)
        sync_files(source_files, destination_files)
        response.status = 200
        return {"message": "Files synced successfully"}
# 优化算法效率
    except Exception as e:
# NOTE: 重要实现细节
        response.status = 500
        return {"error": str(e)}

if __name__ == '__main__':
    # Set the listen address and port
    run(host='localhost', port=8080)
