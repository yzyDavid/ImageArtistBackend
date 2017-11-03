from __future__ import absolute_import
from flask import Flask
from flask import request
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


@app.route('/hello', methods=['GET'])
def hello():
    return 'ImageArtist Backend API'


@app.route('/theme_color', methods=['POST'])
def theme_color():
    if 'image' not in request.files:
        return '', 400
    f = request.files['image']
    if f.filename == '':
        return '', 400
    if not _allowed_file(f.filename):
        return '', 400

    filename = secure_filename(f.filename)
    pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    result = _theme_algorithm.serve({'file': pathname})
    return 'Not Implemented', 200


if __name__ == '__main__':
    _init()
    app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
