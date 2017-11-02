from flask import Flask
from flask import request
import os
from werkzeug.utils import secure_filename

from .config import DEBUG, PORT, TEMP_DIR, ALLOWED_EXTENSIONS
from .theme_algorithm import ThemeAlgorithm

app = Flask(__name__)

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
    f = request.files['image']
    result = _theme_algorithm.serve({'file': f})
    return f, 200


if __name__ == '__main__':
    _init()
    app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
