from flask import Flask, render_template, request, redirect, \
                  url_for, abort, send_from_directory,Response
import time, math
import subprocess
import imghdr
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.xml', '.csv', '.txt','.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index_upload_images.html.jinja', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            return "Invalid file", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/content') # render the content a url differnt from index
def content():
    def inner():
       process = subprocess.Popen(['ping', '-c 400', 'python.org'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

       while True:
          output = process.stdout.readline()
          yield(output.strip()+"<br/>\n")
          # Do something else
          return_code = process.poll()
          if return_code is not None:
              yield('RETURN CODE', return_code+"<br/>\n")
              # Process has finished, read rest of the output 
              for output in process.stdout.readlines():
                 yield(output.strip()+"<br/>\n")
              break

    return Response(inner(), mimetype='text/html')

app.run(debug=True)

