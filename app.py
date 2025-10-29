# app.py

from flask import Flask, render_template, request
import pdfkit

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    html_content = request.form['html_content']
    pdfkit.from_string(html_content, 'output.pdf')
    return 'PDF created!'

if __name__ == '__main__':
    app.run(debug=True)