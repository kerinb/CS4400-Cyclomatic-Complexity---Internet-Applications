import sys

import os

import SharedFunctionLibrary as SFL
from flask import Flask, request
from flask_restful import Api, Resource

ROOT_FOR_REPO = "git_repo/"

app = Flask(__name__)
api = Api(app)

NUM_OF_ACTIVE_WORKERS = 0
CURR_COMMIT_POS = 0
LIST_OF_COMMITS = []
list_of_cc = []


class Manager(Resource):
    def get(self):
        global CURR_COMMIT_POS, LIST_OF_COMMITS
        if len(LIST_OF_COMMITS) > CURR_COMMIT_POS:
            commits = LIST_OF_COMMITS[CURR_COMMIT_POS]
            CURR_COMMIT_POS += 1
            print "commit number:{0}\ncommit file:{1}".format(CURR_COMMIT_POS, commits)
            response = {'commits': commits}
        else:
            response = {'commits': None}
        return response

    def post(self):
        print "HELLO WORLD!\nI am in Manager's post function"
        avg = request.get_json()['avg_cc']
        list_of_cc.append(avg)
        print list_of_cc


class AddNewWorker(Resource):
    def get(self):
        global NUM_OF_ACTIVE_WORKERS
        initial_request_from_worker = request.get_json()['register_wth_manager']
        if initial_request_from_worker is True:
            dir_to_clone_into = 'Worker{0}'.format(NUM_OF_ACTIVE_WORKERS)
            if not os.path.exists(dir_to_clone_into):
                os.mkdir(dir_to_clone_into)
            SFL.clone_git_repo(dir_to_clone_into)
            response = {'worker_id': NUM_OF_ACTIVE_WORKERS, 'dir': dir_to_clone_into}
            NUM_OF_ACTIVE_WORKERS += 1
        else:
            response = {'worker_id': None, 'dir': None}
        return response


api.add_resource(Manager, '/')
api.add_resource(AddNewWorker, '/add_new_worker')

if __name__ == "__main__":
    global ROOT_FOR_REPO, CURR_COMMIT_POS, LIST_OF_COMMITS
    repo = SFL.clone_git_repo(ROOT_FOR_REPO)

    for commit in repo.iter_commits():
        LIST_OF_COMMITS.append(str(commit))

    app.run(debug=False, host='127.0.0.1', port=5000)
    while NUM_OF_ACTIVE_WORKERS < sys.argv[1]:
        pass
