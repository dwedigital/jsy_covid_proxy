from flask import Flask,request, jsonify
from flask_restful import Api, Resource
from scripts import fetch
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app)
CORS(app,resources={r"/active-cases": {"origins": "chrome-extension://*"},
r"/check-update": {"origins": "chrome-extension://*"}})

@app.errorhandler(429)
def ratelimit_handler(e):
    return {"error":f"ratelimit of {e.description} exceeded "}

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10000 per day", "100 per hour"],
)

class Active(Resource):
    def get(self):
        # try:
        #     if ("chrome-extension://" not in request.headers['Origin'] ):
        #         return {"error":"Invalid request, must be made from valid Chrome extension"}
        # except KeyError:
        #     return {"error":"Invalid request, must be made from valid Chrome extension"}
        return jsonify(fetch.CaseData())


class VaccineData(Resource):
    def get(self):
        return jsonify(fetch.VaccineData())

class Check (Resource):
    def get(self):
        return jsonify(fetch.checkUpdate())



# @limiter.limit("1000 per hour")
# @app.route('/active-cases')
# def getData():
#     try:
#         if ("chrome-extension://" not in request.headers['Origin'] ):
#             return {"error":"Invalid request, must be made from valid Chrome extension"}
#     except KeyError:
#         return {"error":"Invalid request, must be made from valid Chrome extension"}

#     return jsonify(fetch.data())

# @app.route('/check-update')
# def checkUpdate():
#     return jsonify(fetch.checkUpdate())

api.add_resource(Active,'/active-cases')
api.add_resource(Check,'/check-update')
api.add_resource(VaccineData,'/vaccine-data')

    

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
