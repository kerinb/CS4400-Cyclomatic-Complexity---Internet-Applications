import time
import os

import sys

import shutil

import datetime

import SharedFunctionLibrary as SFL
from flask import Flask, request
from flask_restful import Api, Resource

ROOT_FOR_REPO = "git_repo/"

app = Flask(__name__)
api = Api(app)

NUM_OF_ACTIVE_WORKERS = 0
CURRENT_COMMIT_POSITION = 0
NUMBER_OF_REQUIRED_WORKERS = 0
LIST_OF_COMMITS = []
LIST_OF_AVG_CC = []
LIST_OF_TIME_PER_AVG = []
TOTAL_NUMBER_OF_WORKERS = []
end = 0.0
start = 0.0
avg_cc = 0


class Manager(Resource):
    def get(self):
        """
        returns a commit to the worker to calculate the Cyclomatic Complexity (McCabe's Complexity) for a git repository
        specifically my repository for my CS4400-DistributedFileServer project
        :returns the commit each worker needs to calculate the Cyclomatic /McCabe's complexity for
        """
        global CURRENT_COMMIT_POSITION, LIST_OF_COMMITS, start
        if CURRENT_COMMIT_POSITION is 0 and int(NUMBER_OF_REQUIRED_WORKERS) is NUMBER_OF_REQUIRED_WORKERS:
            start = time.time()
            print"started timer at {}".format(datetime.datetime.now())

        if len(LIST_OF_COMMITS) <= CURRENT_COMMIT_POSITION and NUM_OF_ACTIVE_WORKERS is 0:
            shutdown()

        if NUMBER_OF_REQUIRED_WORKERS is NUM_OF_ACTIVE_WORKERS and len(LIST_OF_COMMITS) > CURRENT_COMMIT_POSITION:
            if len(LIST_OF_COMMITS) > CURRENT_COMMIT_POSITION:
                commits = LIST_OF_COMMITS[CURRENT_COMMIT_POSITION]
                CURRENT_COMMIT_POSITION += 1
                print "commit number:{0}".format(CURRENT_COMMIT_POSITION)
                response = {'commits': commits}
            else:
                response = {'commits': None}
        else:
            response = {'commits': -1}
        return response

    def post(self):
        global end, avg_cc
        """
        appends the calculated Cyclomatic /McCabes complexity for a git repository
        :returns nothing
        """
        avg = request.get_json()['avg_cc']
        LIST_OF_AVG_CC.append(avg)
        #print "list_of_avg_cc {}, list_of_commits {}".format(len(LIST_OF_AVG_CC), len(LIST_OF_COMMITS))
        if len(LIST_OF_AVG_CC) is len(LIST_OF_COMMITS):
            end = time.time()
            print"ended timer at {}".format(datetime.datetime.now())


def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


class AddNewWorker(Resource):
    def get(self):
        """
        registers a new worker with the "manager" server.
        A worker id and worker directory are assigned to every worker who registers
        :returns worker_id and worker_directory to newly registered worker
        """
        global NUM_OF_ACTIVE_WORKERS, TOTAL_NUMBER_OF_WORKERS
        initial_request_from_worker = request.get_json()['register_wth_manager']

        if initial_request_from_worker is True:
            print "Spawning a new worker with id: {}".format(NUM_OF_ACTIVE_WORKERS)
            dir_to_clone_into = 'Worker{0}'.format(NUM_OF_ACTIVE_WORKERS)
            if not os.path.exists(dir_to_clone_into):
                os.mkdir(dir_to_clone_into)
            SFL.clone_git_repo(dir_to_clone_into)
            response = {'worker_id': NUM_OF_ACTIVE_WORKERS, 'dir': dir_to_clone_into}
            NUM_OF_ACTIVE_WORKERS += 1
            TOTAL_NUMBER_OF_WORKERS = NUM_OF_ACTIVE_WORKERS
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
        print "Killing worker with id: {}".format(NUM_OF_ACTIVE_WORKERS)
        NUM_OF_ACTIVE_WORKERS -= 1
        print "NUMBER OF ACTIVE CLIENTS: {}".format(NUM_OF_ACTIVE_WORKERS)
        if NUM_OF_ACTIVE_WORKERS is 0:
            shutdown()


api.add_resource(Manager, '/')
api.add_resource(AddNewWorker, '/add_new_worker')


def clean_up_after_last_run():
    global NUMBER_OF_REQUIRED_WORKERS

    if os.path.exists("git_repo/"):
        os.chmod("git_repo/", 0o755)
        shutil.rmtree("git_repo/")
    else:
        print "repo doesnt exist - no need to delete"
    for i in range(0, NUMBER_OF_REQUIRED_WORKERS):
        path = "Worker{}".format(i)
        if os.path.exists(path):
            os.chmod(path, 0o755)
            shutil.rmtree(path)
            print "removed repo {}".format(path)


if __name__ == "__main__":
    NUMBER_OF_REQUIRED_WORKERS = int(sys.argv[1])
    print "waiting for {} workers to connect".format(NUMBER_OF_REQUIRED_WORKERS)
    clean_up_after_last_run()
    repo = SFL.clone_git_repo(ROOT_FOR_REPO)
    headers = "'TOTAL_NUMBER_OF_WORKERS', 'SUM_OF_TIME_TAKEN', 'TIME_TAKEN_TO_RUN', 'AVG_CC'\n"
    with open("individual_results.txt", "a+") as ind_res:
        data = ind_res.read()
        if not data:
            ind_res.write(str(headers))
        ind_res.close()

    for commit in repo.iter_commits():
        LIST_OF_COMMITS.append(str(commit))

    app.run(debug=False, host='127.0.0.1', port=5000)

    total_time = end - start
    cc = 0
    for i in range(len(LIST_OF_AVG_CC)):
        cc += LIST_OF_AVG_CC[i]
    avg_cc = cc/len(LIST_OF_AVG_CC)
    ind_data = "{}, {}, {}, {}\n".format(
        TOTAL_NUMBER_OF_WORKERS, sum(LIST_OF_TIME_PER_AVG), total_time, avg_cc
    )
    with open("individual_results.txt", "r+") as ind_res:
        data = ind_res.read()
        ind_res.write(str(ind_data))
        ind_res.close()
    print "TIME TAKEN TO RUN PROGRAM CC: {}".format(total_time)
