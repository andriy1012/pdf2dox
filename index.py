from flask import Flask, render_template, request, send_file
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates')

# Configure upload folder (in memory for Vercel)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    if file and file.filename.lower().endswith('.pdf'):
        # Use secure filename and in-memory processing
        filename = secure_filename(file.filename)
        
        # Save PDF temporarily
        pdf_path = f"/tmp/{filename}"
        file.save(pdf_path)
        
        # Convert to Word
        docx_path = f"/tmp/{filename.replace('.pdf', '.docx')}"
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        
        # Return the converted file
        return send_file(
            docx_path,
            as_attachment=True,
            download_name=filename.replace('.pdf', '.docx'),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    
    return "Invalid file type", 400

# Vercel requires this to be named 'app'
if __name__ == '__main__':
    app.run()