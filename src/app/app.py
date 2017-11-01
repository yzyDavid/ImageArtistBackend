from flask import Flask

from .config import DEBUG

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    return 'ImageArtist Backend API'


if __name__ == '__main__':
    app.run()
