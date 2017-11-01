from flask import Flask
from flask import request

from .config import DEBUG, PORT

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    return 'ImageArtist Backend API'


@app.route('/theme_color', methods=['POST'])
def theme_color():
    headers = request.headers
    f = request.files['image']


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
