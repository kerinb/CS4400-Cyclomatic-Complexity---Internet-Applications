import flask
import flask_restful

class Worker:
    def __init__(self):
        self.name = 'worker'

    def work(self):
        print "in workers work function"

    def get_work(self):
        print "in workers get work function"


if __name__ == '__main__':
    worker = Worker()
    print "Done Working..."
