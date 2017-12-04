from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Manager(Resource):
    def get(self):
        print "HELLO WORLD!\nI am in Manager's get function"

    def post(self):
        print "HELLO WORLD!\nI am in Manager's post function"


api.add_resource(Manager, '/')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
