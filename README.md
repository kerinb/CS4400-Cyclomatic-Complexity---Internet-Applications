# CS4400 - Internet Applications #
## Distributed Cyclomatic Complexity Calculator##
Breandán Kerin, B.A.I. Computer Engineering, 14310166

This project is the second assignment for the CS4400 Internet Applications module for my final year in Trinity College Dublin. This project
It is an application to calculate the average cyclomatic complexity of a repository online, such as a Github or Bitbucket repository.

A Manager node distributes "work" to a set of Worker nodes, which complete the work that has been assigned to them and return the results to the Manager. There are many patterns of work delegation that are commonly used, but for this application the work-stealing pattern was implemented. This means that the Worker nodes request work from the manager, rather than waiting for work to be assigned to them.


### Dependencies : ###
These dependencies are specified in the requirements_to_compile.txt file. Installing these dependencies is a pre-requisite to launching the Manager and Worker nodes, and so the installation of the dependencies is included in the script manager_startup.sh.
*  flask
*  flask_restful
*  radon (library for calculating the cyclomatic complexity of python files)
*  GitPython
*  Matplotlib ( for plotting results using the plot_results.py script)


### Instructions to Launch ###
This program can be run through an IDE or can be run through terminal, where you can specify the number of workers you wish to spawn, using the following shell scripts:
*   _./manager_startup.sh 5_;  this will i) install the project dependencies, and ii) spawn a manager that will wait for 5 workers to spawn before distributing work.
*   _./worker_startup.sh 5_; this script will spawn the specified number of workers.
   
It is also possible to plot the results obtained after performing a number of runs of this application, using the script _plot_results.py_.


### Overview of Operation ###
Once all workers are online, the Manager will begin to assign successive commits to each of them. They will begin calculating the Cyclomatic Complexity (_CC_) for the commit they are given by
the Manager. Once each worker has completed its calculation, it returns its value for the _CC_ to the Manager, where the
average _CC_ will be calculated for all of the commits in the repository.

The manager and each of the workers will have their own, private copy of the repository in question. These copies of the repository are cloned upon start-up of each of these nodes, and stored in a known directory associated with that node.

For analytic purposes, experiments were carried out in order to determine the speed of the average calculation, and
to compare the speed at which multiple workers can calculate the _CC_ for the repository.

#### The Manager Node ####
The Manager node coordinates the distributed set of worker nodes, enabling increases in the speed of the _CC_ calculation for the repository in question.

The Manager is available at service URL "http://127.0.0.1:5000" once it has launched. Before it gets to this stage, it will have don't some initialisation, described in the next paragraph.

The logic of the Manager is as follows:

* Upon launching, perform the following initialisation:
   * Clean up any old files remaining from a previous run
   * Clone a fresh copy of the repository on which the calculation is being performed, and store it in directory 'git_repo/'
   * Iterate through the commits in this cloned repository, and add each one to a global list of commits.
* Start accepting registration connections from workers at this point, by launching the server at the service URL. The workers are able to register with the manager at the URL http://127.0.0.1:5000/add_new_worker.
   * Once a request is received from a worker, the manager will assign a unique ID to it (a global variable incremented for each new worker).
   * The repository is again cloned for this worker, to a directory 'WorkerX/' where X is the ID of the worker.
   * Upon receipt of it's registration ID and repository directory, the worker will immediately begin polling the manager for work. However, the Manager will not delegate any work to the worker until all of the workers it expects to connect, have connected.
* Once all of the expected number of workers have registered with the manager, the manager begins to delegate work.
   * Each worker is given the SHA hash for a commit in the repository. The commit each worker is given is the commit at the next index in the list of commits.
      * In the case of the first successful request for a commit by a worker, the time is measured and taken to be the start time of the calculation (since this marks the starting point of the calculation of the CC for the repository).
   * Each worker will perform the calculation on its given commit, and return the average CC for the commit as a single number, to the manager.
* Once the number of results that the manager has received is equal to the number of commits it had in the first place, (i.e. when the worker working on the final commit posts its results to the manager), the calculation is finished. 
   * This means that the time is measured again and taken to be the end time of the calculation. The manager now sends the message {'commits':-1} to each of the workers, instructing them to terminate.
   * Each worker responds to this message by sending a post request to the URL http://127.0.0.1:5000/add_new_worker. When it does so, the number of active workers recorded with the server is decremented
* The final calculation is now performed: the calculation of the average CC of the repository.
   * The list of results returned by the workers is iterated through, and added to a running total (the 'total commit complexity').
   * The average complexity for the entire repository is then calculated by dividing this running total by the number of commits in the repository.
* Finally, the manager outputs the results to a file _individual_results.txt_. This file has headings:
   'TOTAL_NUMBER_OF_WORKERS' | 'SUM_OF_TIME_TAKEN' | 'TIME_TAKEN_TO_RUN' | 'AVG_CC'
   * Each of these values is outputted to the file.
   * All of the directories created during the running of the application are now cleaned up and removed in preparation for the next run.


#### The Worker Node ####
The worker node completes a piece of "work" given to it by the Manager. As discussed, in this case the piece of work is the calculation of the average CC of a commit in the given repository.

The workers in this particular project use the _work-stealing pattern_, meaning that they request work from the Manager rather than waiting for the Manager to delegate work to them. Essentially, once registered with the Manager each worker will poll the manager for work until there is none remaining, when they will terminate.

The logic of a worker node is as follows:

*   Initialise by sending a request for an ID and a working directory from the Manager. Note that this requires the Manager to have been launched beforehand.
*   Thereafter, the worker polls the Manager asking for work. The Manager can respond with any one of 3 responses:
   *   {'commits': None} indicates that the Manager is still waiting for other workers to join, and so the worker should wait
   *   {'commits': -1} indicates that there is no more work left to do, and so the worker terminates execution
   *   {'commits': commit} provides the hash corresponding to a commit in the cloned repository, instructing the worker to perform a calculation on the repository at this commit.
*   Once the worker is given work to do:
   *   The worker checks out the repository at the specified commit, and extracts the python files (since non-python files cannot be analysed for cyclomatic complexity by the Radon library)
   *   The worker then iterates over each file in this commit, calculating the cyclomatic complexity and adding the result to a running total.
   *   Once the cyclomatic complexity has been calculated for all files in the commit, the worker calculates the average complexity of the commit by dividing the running total by the number of files in the commit. 
   *   This result is then sent back to the Manager, and the worker proceeds to poll the Manager for more work.
*   Once there is no more work to do, the worker will receive the {'commits': -1} response to a request for more work - an instruction to terminate. The worker responds to this with a post request to the URL http://127.0.0.1:5000/add_new_worker, and then terminates.

#### The Shared Function Library ####
The shared function library contains the shared method and variables to clone the required git repository, which is my own Bitbucket repository for the CS7NS1 Assignment 3 Distributed File System.


### Results ###
The results obtained from the experiments can be viewed in the file _"individual_results.txt"_,  where they are entered
in a CSV format. For the purposes of this investigation, the number of workers spawned increased from 1 to 20 to compare
the difference in the time taken for them to calculate the average _CC_.

![graph](https://bytebucket.org/Breandan96/cs4400cyclomaticcomplexity/raw/8aca4ea9e180e7a5f6bd3ed0ac5bc964b9db4be3/CCplot.png)

With reference to _CCplot.png_, it can be seen that as the number of workers increases from 1, the time taken to calculate
the _CC_ decreases from approximately 3.5 seconds down to 1.75 seconds where it then fluctuates around this value and then begins
to increase again at 16 workers.

From theory of concurrent systems, it is expected that the time would decrease rapidly, plateau off at a particular range, and
then begin to increase again. This is what happens in this scenario, but it should be noted that it was expected that the
time would begin to increase again somewhere around 6 workers.

