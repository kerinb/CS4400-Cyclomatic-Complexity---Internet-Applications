import os
import requests
from radon.cli import CCHarvester, Config
from radon.complexity import SCORE

MANAGER_URL = "http://127.0.0.1:5000"
INITIAL_MANAGER_CALL = "http://127.0.0.1:5000/add_new_worker"
ROOT_FOR_REPO = "git_repo/"


def initial_call_to_manager():
    response = requests.get(INITIAL_MANAGER_CALL, json={'register_wth_manager': True})
    did_registration_work = response.json()['did_it_work']
    worker_id = response.json()['worker_id']
    if did_registration_work is True:
        print "NOTE: new worker has made initial comms with manager\nworker id = {}".format(worker_id)
        return worker_id
    else:
        worker_id = None
        print "ERROR: Worker registration did not work and an error occurred with the manager..." \
              "worker id assigned by manager: {}".format(response.json()['worker_id'])
        return worker_id


def get_files_from_given_commit():
    files_from_commit = []
    for root, dirs, files in os.walk(ROOT_FOR_REPO, topdown=True):
        for file_ in files:
            if file_.endswith('.py'):
                files_from_commit.append(root + '/' + file_)
    return files_from_commit


class Worker:
    cc_config = Config(
        exclude='', ignore='venv', order=SCORE, max='F',
        no_assert=True, show_closures=False, min='A'
    )

    def __init__(self):
        self.name = 'worker'
        self.working = True
        response = initial_call_to_manager()
        if response is not None:
            self.worker_id = response
        else:
            return

    def get_work(self):
        while self.working:
            work_from_manager = requests.get(MANAGER_URL)
            commit = work_from_manager.json()['commits']
            if commit is None:
                break
            elif work_from_manager is not None:
                self.work(commit)
        print "No more work from manager...\nfunction complete..."

    def work(self, commit):
        print "in workers work function"
        total_complexity = 0
        num_files = 0
        files = get_files_from_given_commit()
        for file_ in files:
            file_complexity = 0
            print file_
            open_file = open(file_, 'r')
            cc_results = CCHarvester(file_, self.cc_config).gobble(open_file)
            for cc_res in cc_results:
                file_complexity += int(cc_res.complexity)
            total_complexity += file_complexity
        num_files += 1
        avg_complexity = total_complexity/num_files
        print "Worker {0} calculated total complexity: {1} for commit {2}".format(self.worker_id, total_complexity, commit,)
        print "avg complexity is: {}".format(avg_complexity)

if __name__ == '__main__':
    worker = Worker()
    worker.get_work()
    print "Done Working..."
