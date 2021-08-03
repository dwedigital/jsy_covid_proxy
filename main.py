from flask import Flask,request, jsonify
from scripts import fetch
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app,resources={r"/active-cases": {"origins": "chrome-extension://*"},
r"/check-update": {"origins": "chrome-extension://*"}})

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10000 per day", "100 per hour"],
)


@limiter.limit("1000 per hour")
@app.route('/active-cases')
def getData():
    try:
        if ("chrome-extension://" not in request.headers['Origin'] ):
            return {"error":"Invalid request, must be made from valid Chrome extension"}
    except KeyError:
        return {"error":"Invalid request, must be made from valid Chrome extension"}

    return jsonify(fetch.data())

@app.route('/check-update')
def checkUpdate():
    return jsonify(fetch.checkUpdate())
    
@app.errorhandler(429)
def ratelimit_handler(e):
    return {"error":f"ratelimit of {e.description} exceeded "}
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
