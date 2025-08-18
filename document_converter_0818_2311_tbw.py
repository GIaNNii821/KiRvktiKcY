# 代码生成时间: 2025-08-18 23:11:33
#!/usr/bin/env python

"""
Document Converter

This program uses the Bottle framework to create a simple web service that
converts documents between different formats.
"""

from bottle import Bottle, request, response, run
from io import BytesIO
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.oxml import OxmlElement
import xlsxwriter
import xlsx2csv
import os
import mimetypes


# Create a new Bottle instance
app = Bottle()

"""
Convert a Word document to HTML.
"""
def word_to_html(docx_path):
    doc = Document(docx_path)
    html = "<html><body>"
    for paragraph in doc.paragraphs:
        html += f"<p align='{WD_ALIGN_PARAGRAPH[paragraph.alignment].name}'>{paragraph.text}</p>"
    html += "</body></html>"
    return html

"""
Convert an Excel document to CSV.
"""
def excel_to_csv(xlsx_path):
    csv_path = xlsx_path.replace('.xlsx', '.csv')
    xlsx2csv.convert(xlsx_path, csv_path)
    return csv_path

"""
Handle the document conversion request.
"""
@app.route('/convert', method='POST')
def convert_document():
    try:
        # Check if a document was provided
        if 'file' not in request.files:
            response.status = 400
            return {"error": "No file provided"}

        file = request.files['file']
        if not file.filename:
            response.status = 400
            return {"error": "No filename provided"}

        # Get the file extension and determine the conversion type
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext == 'docx':
            docx_path = 'temp.docx'
            file.save(docx_path)
            html = word_to_html(docx_path)
            os.remove(docx_path)
            response.content_type = 'text/html'
            return html
        elif file_ext == 'xlsx':
            xlsx_path = 'temp.xlsx'
            file.save(xlsx_path)
            csv_path = excel_to_csv(xlsx_path)
            os.remove(xlsx_path)
            with open(csv_path, 'rb') as f:
                response.content_type = 'text/csv'
                return f.read()
        else:
            response.status = 400
            return {"error": "Unsupported file format"}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

"""
Run the Bottle application.
"""
if __name__ == '__main__':
    run(app, host='localhost', port=8080)