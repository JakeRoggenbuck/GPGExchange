import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from database import DataBase


UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'asc', 'pgp', 'gpg', 'jpg', 'png'}

GPG_EXCHANGE = Flask(__name__)
GPG_EXCHANGE.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = DataBase()


# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@GPG_EXCHANGE.route('/')
def home():
    # Pulls all data
    all_data = DATABASE.read_all()
    # Sends all data to template as a list of tuples
    return render_template("home.html", files=all_data)


# Sets route for individual files
@GPG_EXCHANGE.route('/files/<string:filename>')
def get_file(filename):
    file_path = GPG_EXCHANGE.config['UPLOAD_FOLDER']
    return send_file(os.path.join(file_path, filename), as_attachment=True)


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

        # Checks if file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = GPG_EXCHANGE.config['UPLOAD_FOLDER']
            full_path = os.path.join(file_path, filename)
            file.save(full_path)

            # Gets values from form
            title = request.form['title']
            description = request.form['description']
            email = request.form['email']
            DATABASE.write(title, description, email, filename)
            # Redirect to file, uses route /files/filename
            return redirect(url_for('upload_file', filename=filename))

    return render_template("upload.html")


if __name__ == "__main__":
    GPG_EXCHANGE.run()
