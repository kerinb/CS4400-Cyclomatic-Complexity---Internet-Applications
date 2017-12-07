import os
import requests
import time
from git import Repo
from radon.cli import CCHarvester, Config
from radon.complexity import SCORE

MANAGER_URL = "http://127.0.0.1:5000"
INITIAL_MANAGER_CALL = "http://127.0.0.1:5000/add_new_worker"


def initial_call_to_manager():
    response = requests.get(INITIAL_MANAGER_CALL, json={'register_wth_manager': True})
    worker_id = response.json()['worker_id']
    working_dir = response.json()['dir']
    return worker_id, working_dir


def get_files_from_given_commit(repo_dir, commit):
    repo = Repo(repo_dir).git
    repo.checkout(commit)
    files_from_commit = []
    for root, dirs, files in os.walk(repo_dir, topdown=True):
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
        self.working = True
        self.worker_id = response, self.working_dir = initial_call_to_manager()

    def get_work(self):
        while self.working:
            work_from_manager = requests.get(MANAGER_URL)
            commit = work_from_manager.json()['commits']
            if commit is None:
                break
            elif commit is -1:
                # wait until all workers have cloned the repo
                self.working = False
            elif work_from_manager is not None:
                start = time.time()
                avg_cc = self.work(commit)
                end = time.time()
                time_taken_over_commit = end - start
                requests.post(MANAGER_URL,  json={'avg_cc': avg_cc, 'time': time_taken_over_commit})
        print "No more work from manager...\nfunction complete..."
        return self.worker_id

    def work(self, commit):
        total_complexity = 0
        num_files = 0
        files = get_files_from_given_commit(self.working_dir, commit)

        for file_ in files:
            file_complexity = 0
            print file_
            open_file = open(file_, 'r')
            cc_results = CCHarvester(file_, self.cc_config).gobble(open_file)

            for cc_res in cc_results:
                file_complexity += int(cc_res.complexity)
            total_complexity += file_complexity
        num_files += 1
        avg_complexity = total_complexity / num_files
        print "Worker{}\n".format(self.worker_id)
        print "avg complexity is: {}".format(avg_complexity)
        return avg_complexity


def shutdownWorker():
    requests.post(INITIAL_MANAGER_CALL)


if __name__ == '__main__':
    worker = Worker()
    wid = worker.get_work()
    print "Worker{} done Working...".format(wid)
    shutdownWorker()
