from flask import Flask

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'ImageArtist Backend API'


if __name__ == '__main__':
    app.run()
