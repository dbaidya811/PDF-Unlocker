from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import threading
from pypdf import PdfReader, PdfWriter
import time

app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = 'uploads'
UNLOCKED_FOLDER = 'unlocked'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UNLOCKED_FOLDER, exist_ok=True)

jobs = {}

def unlock_pdf(filepath, job_id):
    try:
        reader = PdfReader(filepath)
        if not reader.is_encrypted:
            # Save the file directly to unlocked folder since it's not encrypted
            output_path = os.path.join(UNLOCKED_FOLDER, f'unlocked_{job_id}.pdf')
            with open(output_path, 'wb') as f:
                with open(filepath, 'rb') as src_file:
                    f.write(src_file.read())
            jobs[job_id] = {
                'status': 'success', 
                'file': output_path,
                'message': 'PDF was not encrypted',
                'password': 'No password needed'
            }
            return
    except Exception as e:
        jobs[job_id] = {
            'status': 'error',
            'message': f'Error processing PDF: {str(e)}'
        }
        return

    start_time = time.time()
    counter = 0
    
    # Try 4-digit passwords (0000 to 9999)
    for length in [4, 5, 6]:
        max_value = 10 ** length
        for i in range(0, max_value):
            password = str(i).zfill(length)
            
            # Print current password being tried
            print(f"Trying password: {password}")
            
            if reader.decrypt(password):
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                
                output_path = os.path.join(UNLOCKED_FOLDER, f'unlocked_{job_id}.pdf')
                with open(output_path, 'wb') as f:
                    writer.write(f)
                
                jobs[job_id] = {'status': 'success', 'file': output_path, 'password': password}
                return
            
            counter += 1
            
            # Calculate and display rate every 25 attempts
            if counter % 25 == 0:
                elapsed = time.time() - start_time
                rate = counter / elapsed if elapsed > 0 else 0
                print(f"Passwords tried: {counter}, Rate: {rate:.2f} per second")
    
    jobs[job_id] = {'status': 'failed', 'message': 'Password not found'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File is not a PDF'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Check if PDF is encrypted
    try:
        reader = PdfReader(filepath)
        if not reader.is_encrypted:
            # If not encrypted, return success immediately
            job_id = str(len(jobs))
            output_path = os.path.join(UNLOCKED_FOLDER, f'unlocked_{job_id}.pdf')
            with open(output_path, 'wb') as f:
                with open(filepath, 'rb') as src_file:
                    f.write(src_file.read())
            
            jobs[job_id] = {
                'status': 'success',
                'file': output_path,
                'message': 'PDF was not encrypted',
                'password': 'No password needed'
            }
            return jsonify({
                'job_id': job_id,
                'status': 'success',
                'message': 'PDF was not encrypted'
            })
    except Exception as e:
        return jsonify({'error': f'Error checking PDF: {str(e)}'}), 400
    
    # If we get here, the PDF is encrypted and needs processing
    job_id = str(len(jobs))
    jobs[job_id] = {'status': 'processing'}
    
    # Start the password cracking in a separate thread
    thread = threading.Thread(target=unlock_pdf, args=(filepath, job_id))
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'processing'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status/<job_id>')
def check_status(job_id):
    job = jobs.get(job_id, {})
    return jsonify(job)

@app.route('/download/<job_id>')
def download_file(job_id):
    job = jobs.get(job_id, {})
    if job.get('status') == 'success':
        return send_file(job['file'], as_attachment=True)
    return jsonify({'error': 'File not ready or not found'}), 404

if __name__ == '__main__':
    app.run(threaded=True)
