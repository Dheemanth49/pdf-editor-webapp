import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'supersecretkey'

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('merge_files')
    pdf_writer = PdfWriter()
    for file in files:
        if file and allowed_file(file.filename):
            reader = PdfReader(file)
            for page in reader.pages:
                pdf_writer.add_page(page)
    output = BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='merged.pdf', mimetype='application/pdf')

@app.route('/split', methods=['POST'])
def split_pdf():
    file = request.files['split_file']
    if file and allowed_file(file.filename):
        reader = PdfReader(file)
        outputs = []
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            out = BytesIO()
            writer.write(out)
            out.seek(0)
            outputs.append((f'page_{i+1}.pdf', out.read()))
        # For simplicity, return first page. (Can be zipped for all pages)
        return send_file(BytesIO(outputs[0][1]), as_attachment=True, download_name=outputs[0][0], mimetype='application/pdf')
    flash('Invalid PDF file.')
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_pages():
    file = request.files['delete_file']
    pages_str = request.form.get('delete_pages') # e.g., "1,3,5"
    if file and allowed_file(file.filename) and pages_str:
        reader = PdfReader(file)
        total = len(reader.pages)
        to_delete = set(int(num.strip()) - 1 for num in pages_str.split(',') if num.strip().isdigit())
        writer = PdfWriter()
        for i, page in enumerate(reader.pages):
            if i not in to_delete:
                writer.add_page(page)
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='deleted.pdf', mimetype='application/pdf')
    flash('Please provide a valid PDF and pages to delete.')
    return redirect(url_for('index'))

@app.route('/rotate', methods=['POST'])
def rotate_pages():
    file = request.files['rotate_file']
    angle = int(request.form.get('rotate_angle', 0))
    pages_str = request.form.get('rotate_pages') # e.g., "1,2"
    if file and allowed_file(file.filename) and pages_str and angle in [90, 180, 270]:
        reader = PdfReader(file)
        to_rotate = set(int(num.strip()) - 1 for num in pages_str.split(',') if num.strip().isdigit())
        writer = PdfWriter()
        for i, page in enumerate(reader.pages):
            if i in to_rotate:
                page.rotate(angle)
            writer.add_page(page)
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='rotated.pdf', mimetype='application/pdf')
    flash('Please provide a valid PDF, pages, and angle (90, 180, 270).')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)