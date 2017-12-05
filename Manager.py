import time
import os
import SharedFunctionLibrary as SFL
from flask import Flask, request
from flask_restful import Api, Resource

ROOT_FOR_REPO = "git_repo/"

app = Flask(__name__)
api = Api(app)

NUM_OF_ACTIVE_WORKERS = 0
CURRENT_COMMIT_POSITION = 0
LIST_OF_COMMITS = []
LIST_OF_AVG_CC = []


class Manager(Resource):
    def get(self):
        """
        returns a commit to the worker to calculate the Cyclomatic Complexity (McCabe's Complexity) for a git repository
        specifically my repository for my CS4400-DistributedFileServer project
        :returns the commit each worker needs to calculate the Cyclomatic /McCabe's complexity for
        """
        global CURRENT_COMMIT_POSITION, LIST_OF_COMMITS
        if len(LIST_OF_COMMITS) > CURRENT_COMMIT_POSITION:
            commits = LIST_OF_COMMITS[CURRENT_COMMIT_POSITION]
            CURRENT_COMMIT_POSITION += 1
            print "commit number:{0}".format(CURRENT_COMMIT_POSITION)
            response = {'commits': commits}
        else:
            response = {'commits': None}
        return response

    def post(self):
        """
        appends the calculated Cyclomatic /McCabes complexity for a git repository
        :returns nothing
        """
        avg = request.get_json()['avg_cc']
        LIST_OF_AVG_CC.append(avg)
        print sum(LIST_OF_AVG_CC)/len(LIST_OF_AVG_CC)


class AddNewWorker(Resource):
    def get(self):
        """
        registers a new worker with the "manager" server.
        A worker id and worker directory are assigned to every worker who registers
        :returns worker_id and worker_directory to newly registered worker
        """
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

    def post(self):
        global NUM_OF_ACTIVE_WORKERS
        """
        this function is used to simply decrement thw number of workers alive - when this reaches zero, the Cyclomatic/
        McCabe's complexity is then calculated and the server can die with a user input; so we wont lose the results.
        :return: nothing 
        """
        NUM_OF_ACTIVE_WORKERS -= 1
        print "NUMBER OF ACTIVE CLIENTS: {}".format(NUM_OF_ACTIVE_WORKERS)
        if NUM_OF_ACTIVE_WORKERS is 0:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

api.add_resource(Manager, '/')
api.add_resource(AddNewWorker, '/add_new_worker')

if __name__ == "__main__":
    repo = SFL.clone_git_repo(ROOT_FOR_REPO)

    for commit in repo.iter_commits():
        LIST_OF_COMMITS.append(str(commit))

    start = time.time()
    app.run(debug=False, host='127.0.0.1', port=5000)
    end = time.time()
    time_taken = end - start
    print "TIME TAKEN TO CALCULATE CC: {}".format(time_taken)
