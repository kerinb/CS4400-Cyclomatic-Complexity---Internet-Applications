import requests

MANAGER_URL = "http://127.0.0.1:5000"
INITIAL_MANAGER_CALL = "http://127.0.0.1:5000/add_new_worker"


def initial_call_to_manager():
    response = requests.get(INITIAL_MANAGER_CALL, json={'register_wth_manager': True})
    worker_id = response.json()['worker_id']
    print "NOTE: new worker has made initial comms with manager\nworker id = {}".format(worker_id)
    return worker_id


class Worker:
    def __init__(self):
        self.name = 'worker'
        self.working = True
        self.worker_id = initial_call_to_manager()

    def get_work(self):
        print "in workers get work function"
        while self.working:
            work_from_manager = requests.get(MANAGER_URL)
            if work_from_manager is False:
                break
            elif work_from_manager is not None:
                files = work_from_manager.json()['files']
                self.work(files)
        print "No more work from manager...\nfunction complete..."

    def work(self, files):
        print "in workers work function"


if __name__ == '__main__':
    worker = Worker()
    worker.get_work()
    print "Done Working..."
