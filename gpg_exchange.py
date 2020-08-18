import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from database import DataBase


UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'asc', 'pgp', 'gpg'}

GPG_EXCHANGE = Flask(__name__)
GPG_EXCHANGE.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = DataBase()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@GPG_EXCHANGE.route('/')
def home():
    # Pulls all data
    all_data = DATABASE.read_all()
    # Sends all data to template as a list of tuples
    return render_template("home.html", files=all_data)


@GPG_EXCHANGE.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = GPG_EXCHANGE.config['UPLOAD_FOLDER']
            full_path = os.path.join(file_path, filename)
            file.save(full_path)
            return redirect(url_for('upload_file', filename=filename))

    return render_template("upload.html")


if __name__ == "__main__":
    GPG_EXCHANGE.run()
