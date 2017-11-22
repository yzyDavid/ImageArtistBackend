from __future__ import absolute_import
from flask import Flask, Response
from flask import request, send_file
import os
from flask_request_params import bind_request_params
from flask_cors import CORS, cross_origin

from app.config import DEBUG, PORT, TEMP_DIR, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
from app.theme_algorithm import ThemeAlgorithm
from app.style_algorithm import StyleAlgorithm
from app.utils import hash_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = TEMP_DIR
app.before_request(bind_request_params)
CORS(app)

_theme_algorithm = ThemeAlgorithm()
_style_algorithm = StyleAlgorithm()


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def _init():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)


_init()


@app.route('/api/hello', methods=['GET'])
def hello():
    if 'q' in request.args.keys():
        return request.args.get('q')
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

    filename = hash_filename(f)
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

    filename = hash_filename(f)
    pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(pathname)
    result = _theme_algorithm.serve({'file': pathname, 'count': n})

    response = send_file(result, mimetype='image/jpeg', as_attachment=False)
    return response


@app.route('/api/upload_image', methods=['POST'])
@cross_origin()
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

    # filename = secure_filename(f.filename)
    filename = hash_filename(f)
    pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(pathname)

    return pathname


@app.route('/api/upload_style', methods=['POST'])
def upload_style():
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

    filename = hash_filename(f)
    pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(pathname)

    return pathname


@app.route('/api/transfer', methods=['POST'])
def transfer():
    """
    form-data:
    img: str => pathname of an uploaded content image.
    style: str => pathname of an uploaded style image.
    :return: download a jpeg image
    """
    if 'img' not in request.form or 'style' not in request.form:
        return '', 400
    img = request.form['img']
    style = request.form['style']
    if not os.path.exists(img) or not os.path.exists(style):
        return '', 400

    output_pathname = _style_algorithm.serve({'img': img, 'style': style})
    return send_file(output_pathname, mimetype='image/jpeg', as_attachment=False)


@app.route('/api/transfer_url', methods=['POST'])
def transfer_url():
    """
    form-data:
    img: str => pathname of an uploaded content image.
    style: str => pathname of an uploaded style image.
    :return: a jpeg image url
    """
    if 'img' not in request.form or 'style' not in request.form:
        return '', 400
    img = request.form['img']
    style = request.form['style']
    if not os.path.exists(img) or not os.path.exists(style):
        return '', 400

    output_pathname = _style_algorithm.serve({'img': img, 'style': style})
    return output_pathname, 200


@app.route('/api/image', methods=['GET'])
def image():
    if 'q' not in request.args.keys():
        return '', 400
    pathname = request.args.get('q')
    if not pathname.startswith(TEMP_DIR):
        return '', 400
    return send_file(pathname, mimetype='image/jpeg', as_attachment=False)


if __name__ == '__main__':
    _init()
    app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
