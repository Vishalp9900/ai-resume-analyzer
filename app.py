from flask import Flask, render_template, request, jsonify
import os
import tempfile
from analyzer import analyze_resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', tempfile.gettempdir())
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['resume']
    job_desc = request.form.get('job_desc', '').strip()
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.pdf',
        dir=app.config['UPLOAD_FOLDER'],
    )
    path = temp_file.name
    temp_file.close()
    try:
        file.save(path)
        result = analyze_resume(path, job_desc)
        return jsonify(result)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
