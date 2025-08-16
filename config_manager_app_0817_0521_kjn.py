# 代码生成时间: 2025-08-17 05:21:02
# config_manager_app.py
# This is a simple Bottle Web application to manage configuration files.

"""
Configuration Manager Application using Bottle Framework
Purpose: To serve and manage configuration files through HTTP requests.
"""

from bottle import Bottle, request, response, run
import os
import json
from datetime import datetime

# Initialize Bottle app
app = Bottle()

# Define the path to store configuration files
CONFIG_DIR = './configs'

# Ensure the configuration directory exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Utility function to generate a unique filename for a new config
def generate_filename():
    return datetime.now().strftime('%Y%m%d%H%M%S') + '.json'

# Utility function to load configuration from file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        response.status = 404
        return {'error': 'Configuration file not found'}
    except json.JSONDecodeError:
        response.status = 400
        return {'error': 'Invalid JSON format'}

# Utility function to save configuration to file
def save_config(file_path, config):
    try:
        with open(file_path, 'w') as file:
            json.dump(config, file, indent=4)
        return True
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

@app.route('/config', method='GET')
def serve_config():
    """Serve the latest configuration file"""
    files = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
    if not files:
        response.status = 404
        return {'error': 'No configuration files found'}
    # Serve the latest file
    latest_file = sorted(files, reverse=True)[0]
    file_path = os.path.join(CONFIG_DIR, latest_file)
    return load_config(file_path)

@app.route('/config', method='POST')
def create_config():
    """Create a new configuration file with the provided data"""
    file_name = generate_filename()
    file_path = os.path.join(CONFIG_DIR, file_name)
    if 'config' not in request.json:
        response.status = 400
        return {'error': 'Missing configuration data'}
    config = request.json['config']
    result = save_config(file_path, config)
    if isinstance(result, dict):  # An error happened
        return result
    response.status = 201
    response.content_type = 'application/json'
    return {'status': 'Configuration saved successfully', 'file_path': file_path}

@app.route('/config/<filename:path>', method='GET')
def get_config(filename):
    """Get a specific configuration file by filename"""
    file_path = os.path.join(CONFIG_DIR, filename)
    return load_config(file_path)

@app.route('/config/<filename:path>', method='PUT')
def update_config(filename):
    """Update a specific configuration file"""
    file_path = os.path.join(CONFIG_DIR, filename)
    if not os.path.exists(file_path):
        response.status = 404
        return {'error': 'Configuration file not found'}
    if 'config' not in request.json:
        response.status = 400
        return {'error': 'Missing configuration data'}
    config = request.json['config']
    result = save_config(file_path, config)
    if isinstance(result, dict):  # An error happened
        return result
    response.status = 200
    response.content_type = 'application/json'
    return {'status': 'Configuration updated successfully'}

@app.route('/config/<filename:path>', method='DELETE')
def delete_config(filename):
    """Delete a specific configuration file"""
    file_path = os.path.join(CONFIG_DIR, filename)
    try:
        os.remove(file_path)
        response.status = 200
        return {'status': 'Configuration file deleted successfully'}
    except FileNotFoundError:
        response.status = 404
        return {'error': 'Configuration file not found'}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

# Run the Bottle application
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
