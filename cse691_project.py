import os
from flask import Flask, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from transform_video import process_video

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['mp4', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_file(filename):
    abs_in_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'], filename)
    abs_out_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), app.config['PROCESSED_FOLDER'], filename)
    process_video(
        abs_in_filename, '/Users/nagaprasad/Downloads/fast-style-transfer-master/examples/style/la_muse.ckpt',
        abs_out_filename)
    return redirect('/static/'+filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.dirname(os.path.abspath(__file__)))
            file.save(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'], filename))
            return process_file(filename)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
