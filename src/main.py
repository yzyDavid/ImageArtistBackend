from __future__ import absolute_import
from flask import Flask, Response
from flask import request, send_file
import os
from werkzeug.utils import secure_filename

from app.config import DEBUG, PORT, TEMP_DIR, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
from app.theme_algorithm import ThemeAlgorithm

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = TEMP_DIR

_theme_algorithm = ThemeAlgorithm()


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def _init():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)


_init()


@app.route('/api/hello', methods=['GET'])
def hello():
    return 'ImageArtist Backend API'


@app.route('/api/theme_color', methods=['POST'])
def theme_color():
    """
    POST
    form-data:
    image: a jpeg picture
    :return: a jpeg picture download
    """
    if 'image' not in request.files:
        return '', 400
    f = request.files['image']
    if f.filename == '':
        return '', 400
    if not _allowed_file(f.filename):
        return '', 400

    filename = secure_filename(f.filename)
    pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(pathname)
    result = _theme_algorithm.serve({'file': pathname})

    response = send_file(result, mimetype='image/jpeg', as_attachment=True)
    return response


@app.route('/api/theme_color_count', methods=['POST'])
def theme_color_count():
    """
    POST
    form-data:
    image: a jpeg picture
    count: a number, the K of K-means
    :return: a jpeg picture download
    """
    if 'image' not in request.files:
        return '', 400
    f = request.files['image']
    if f.filename == '':
        return '', 400
    if not _allowed_file(f.filename):
        return '', 400

    if 'count' not in request.form:
        return '', 400
    n = request.form['count']
    if type(n) != int:
        n = int(n)
    if n <= 0 or n > 100:
        return '', 400

    filename = secure_filename(f.filename)
    pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(pathname)
    result = _theme_algorithm.serve({'file': pathname, 'count': n})

    response = send_file(result, mimetype='image/jpeg', as_attachment=True)
    return response


@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    """
    form-data:
    image: a jpeg picture
    :return: a file pathname, assigned by backend.
    """
    if 'image' not in request.files:
        return '', 400
    f = request.files['image']
    if f.filename == '':
        return '', 400
    if not _allowed_file(f.filename):
        return '', 400


@app.route('/api/upload_style', methods=['POST'])
def upload_style():
    """
    form-data:
    image: a jpeg picture
    :return: a file pathname, assigned by backend.
    """
    pass


@app.route('/api/transfer', methods=['GET'])
def transfer():
    pass


if __name__ == '__main__':
    _init()
    app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
