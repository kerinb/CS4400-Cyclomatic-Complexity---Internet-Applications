# CS4400 - Internet Applications #
## Distributed Cyclomatic Complexity Calculator##

This project is the second assignment for the CS4400 Internet Applications module for my final year in Trinity College Dublin. This project
Is used to calculate the cyclomatic complexity of a repository online, such as Git.

### dependencies for project: ###
*  flask
*  flask_restful
*  radon
*  GitPython
*  Matplotlib ( for plotting your results using the plot_results.py script)

### Note ###
1: I have had issues with downloading and install pygit2 - so I am using GitPython.
2: This program can be run through an IDE or can be run through terminal, where you can specify the number of workers
   you wish to spawn, using the following:
   _./manager_startup.sh 5_;  this will create a manager that will wait for 5 workers to spawn before distributing work.
   _./worker_startup.sh 5_; this will run a for loop that will spawn the specified number of workers.

Once all workers are online, they will begin calculating the Cyclomatic Complexity (_CC_) for the commit they are given by
the manager. Once the worker has completed its calculation, it returns its value for the _CC_ to the manager, where the
average _CC_ will be calculated for the repository.

For analytic purposes, experiments were carried out in order to determine the speed of the average calculation, and
to compare the speed at which multiple workers can calculate the _CC_ for the repository.

### Results ###
The results obtained from the experiments can be viewed in the file _"individual_results.txt"_,  where they are entered
in a CSV format. For the purposes of this investigation, the number of workers spawned increased from 1 to 20 to compare
the difference in the time taken for them to calculate the average _CC_.

With reference to _CCplot.png_, it canbe seen that as the number of workers increases from 1, the time taken to calculate
the _CC_ decreases from approximately 3.5 s down to 1.75 seconds where it then fluctuates around this value and then begins
to increase at 16 workers.

From theory of concurrent system, it is expected that the time would decrease rapidly, plateau off at a particular range, and
then begin to increase again. This is what happens in this scenario, but it should be noted, that it was expected that the
time would begin to increase again somewhere around 6 workers.

