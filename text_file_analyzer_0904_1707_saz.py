# 代码生成时间: 2025-09-04 17:07:08
#!/usr/bin/env python
{
    "code": """
from bottle import route, run, request, response, static_file
import re
import os

# Define the path to the directory containing the text files
TEXT_FILES_DIR = './text_files'

class TextFileAnalyzer:
    """
    A class responsible for analyzing text files and providing statistics.
    """
    def __init__(self, directory):
        self.directory = directory

    def analyze_file(self, filename):
        """
        Analyze a given text file and return a dictionary with statistics.
        """
        if not os.path.isfile(os.path.join(self.directory, filename)):
            raise FileNotFoundError(f"No file named {filename} found in {self.directory}")

        with open(os.path.join(self.directory, filename), 'r', encoding='utf-8') as file:
            content = file.read()

        # Basic statistics
        words_count = len(re.findall(r'\w+', content))
        lines_count = content.count('
') + 1
        paragraphs_count = content.count('

') + 1

        return {
            'word_count': words_count,
            'line_count': lines_count,
            'paragraph_count': paragraphs_count,
        }

# Set up Bottle app
app = BottleApp()

# Route for serving static files (e.g., HTML, JS, CSS)
@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='static')

# Route for uploading and analyzing a text file
@route('/upload', method='POST')
def upload_and_analyze():
    try:
        # Check if the file is uploaded
        if 'file' not in request.files:
            response.status = 400
            return {'error': 'No file uploaded'}

        # Get the uploaded file
        uploaded_file = request.files['file']
        filename = uploaded_file.filename

        # Save the file to the directory
        file_path = os.path.join(TEXT_FILES_DIR, filename)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.file.read())

        # Analyze the file and get statistics
        analyzer = TextFileAnalyzer(TEXT_FILES_DIR)
        stats = analyzer.analyze_file(filename)

        # Return the statistics as JSON
        return {'filename': filename, 'statistics': stats}

    except FileNotFoundError as e:
        response.status = 404
        return {'error': str(e)}
    except Exception as e:
        response.status = 500
        return {'error': 'An error occurred while processing the file'}

# Run the Bottle app
if __name__ == '__main__':
    run(host='localhost', port=8080)
"""
}
