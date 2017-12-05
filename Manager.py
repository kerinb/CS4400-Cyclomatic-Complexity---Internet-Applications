import radon
from flask import Flask, request
import requests
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

NUM_OF_ACTIVE_WORKERS = 0


class Manager(Resource):
    def get(self):
        print "HELLO WORLD!\nI am in Manager's get function"

    def post(self):
        print "HELLO WORLD!\nI am in Manager's post function"


class AddNewWorker(Resource):
    def get(self):
        global NUM_OF_ACTIVE_WORKERS
        print "in AddNewWorker method in Manager folder"
        initial_request_from_worker = request.get_json()['register_wth_manager']
        if initial_request_from_worker is True:
            response={'worker_id': NUM_OF_ACTIVE_WORKERS, 'did_it_work': True}
            NUM_OF_ACTIVE_WORKERS += 1
        else:
            response={'worker_id': None, 'did_it_work': False}
        return response


api.add_resource(Manager, '/')
api.add_resource(AddNewWorker, '/add_new_worker')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
