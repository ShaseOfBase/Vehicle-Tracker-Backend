from app import app
from waitress import serve
from flask_cors import CORS

if __name__ == '__main__':
    CORS(app)
    serve(app, host='127.0.0.1', port=8030)
