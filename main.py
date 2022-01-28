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
    return render_template('index_upload.html.jinja', files=files)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            return redirect(url_for('download_file', name=filename))
    return ''


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

