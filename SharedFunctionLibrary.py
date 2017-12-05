import os
from git import Repo

CLONED_GIT_REPOSITORY = "https://bitbucket.org/Breandan96/cs4400distributedfileserver/commits/all"
BASE_PATH_TO_REPO = "https://bitbucket.org/Breandan96/cs4400distributedfileserver"


def clone_git_repo(path_to_local_repo):
    print 'in git clone repo function in utilities\n Requested to clone{}'.format(CLONED_GIT_REPOSITORY)
    print 'verifying the requested location exists...'
    if not os.path.exists(path_to_local_repo):
        os.mkdir(path_to_local_repo)
        print "make folder for repo"
    if not os.listdir(path_to_local_repo):
        repo = Repo.clone_from(CLONED_GIT_REPOSITORY, path_to_local_repo)
        print "repo cloned..."
    else:
        repo = Repo(path_to_local_repo)
        print "got repo"
    return repo


def get_commits():
    pass
