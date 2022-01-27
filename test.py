from flask import Flask, render_template, Response
import time, math
import subprocess


app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html.jinja') # render a template at the index. The content will be embedded in this template

app.run(debug=True)

