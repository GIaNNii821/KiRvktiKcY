# 代码生成时间: 2025-09-09 21:37:57
#!/usr/bin/env python

"""
Image Resizer Application using Bottle Framework
This application allows users to upload multiple images and resize them to a specified
dimension. The resized images are then saved to the server.
"""

import os
from bottle import route, run, request, response, static_file
from PIL import Image
from io import BytesIO

# Define the directory where uploaded images will be stored temporarily
UPLOAD_FOLDER = 'uploads'

# Define the directory where resized images will be saved
RESIZED_FOLDER = 'resized'

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESIZED_FOLDER, exist_ok=True)

# Define the route for the index page
@route('/')
def index():
    return static_file('index.html', root='.')

# Define the route to handle image uploads
@route('/upload', method='POST')
def upload():
    '''
    Handle the uploaded images and resize them.
    
    Returns a list of URLs to the resized images.
    '''
    try:
        # Get the uploaded files from the request
        uploaded_files = request.files.getall('files')
        
        # Define the target size for resizing
        target_size = request.forms.get('size', type=int)
        
        # Initialize a list to store the URLs of the resized images
        resized_image_urls = []
        
        for file in uploaded_files:
            # Open the image file
            image = Image.open(file)
            
            # Resize the image
            image = image.resize((target_size, target_size))
            
            # Create a buffer to hold the resized image data
            image_buffer = BytesIO()
            image.save(image_buffer, format='JPEG')
            image_buffer.seek(0)
            
            # Get the filename of the uploaded file
            filename = file.filename
            
            # Define the path for the resized image
            resized_path = os.path.join(RESIZED_FOLDER, filename)
            
            # Save the resized image to the server
            with open(resized_path, 'wb') as resized_file:
                resized_file.write(image_buffer.read())
                
            # Append the URL to the resized image to the list
            resized_image_urls.append('/{}/{}'.format(RESIZED_FOLDER, filename))
        
        # Set the response type to JSON
        response.content_type = 'application/json'
        
        # Return the list of URLs to the resized images as JSON
        return {{"resized_images": resized_image_urls}}
    
    except Exception as e:
        # Handle any exceptions and return an error message
        return {{"error": str(e)}}

# Run the Bottle application
run(host='localhost', port=8080)