import matplotlylib.pyplot as plt
from numpy import genfromtxt


def plot_results():
    my_data = genfromtxt('individual_results.txt', delimiter=',', skip_header=1, usecols=[0, 2])
    # print my_data
    x_data = my_data[:, 0]
    y_data = my_data[:, 1]
    print y_data
    plot_my_data(x_data, y_data)


def plot_my_data(x_data, y_data):
    print('making plot')

    fig, bx = plt.subplots()
    bx.scatter(x_data, y_data, edgecolors=(0, 0, 0), color='red')
    bx.set_xlabel('Measured')
    bx.set_ylabel('Predicted')
    plt.savefig('results_plot.png')

if __name__ == '__main__':
    plot_results()
