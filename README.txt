This project is for the CS4400 Internet Applications module in my final year in Trinity College Dublin. This project
Is used to calculate the cyclomatic complexity of a repository online, such as Git.

dependencies for project:
1: flask
2: flask_restful
3: radon
4: GitPython

Note:
1: I have had issues with downloading and install pygit2 - hence I am using GitPython.
2: This program can be run through an IDE or can be run through terminal, where you can specify the number of workers
   you wish to spawn.

Notes on my results:
1: Just having a quick look at my results, its strange that as the number of workers increase the time taken to
execute takes longer. From theory, I would have expected that as the number of workers increased, the time taken would
have decreased up until a certain number of workers. My inkling is that since for each worker since I am downloading my
git repo for each worker, thats where the excess time taken is coming from.
I want to try make the "git_repo" folder global and see if each worker took a branch from that would it reduce the time
taken over the total.