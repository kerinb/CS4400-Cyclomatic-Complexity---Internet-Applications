import requests

MANAGER_URL = "http://127.0.0.1:5000"


class Worker:
    def __init__(self):
        self.name = 'worker'
        self.working = True

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
    worker.work()
    print "Done Working..."
