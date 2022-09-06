from app import app
from waitress import serve
from flask_cors import CORS

if __name__ == '__main__':
    CORS(app)
   # app.run(host="0.0.0.0", port=8030, debug=True)
    serve(app, host='127.0.0.1', port=8030)
