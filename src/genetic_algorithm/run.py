'''Launcher.'''

import argparse
from genetic_algorithm.core.utils import read_params
from genetic_algorithm.core.algorithm import algorithm

if __name__ == "__main__":

    # define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("params", type=str, 
                        help="path to the yaml file defining parameters")
    args = parser.parse_args()

    # read parameters
    params = read_params(args.params)

    # run the algorithm
    algorithm(params)
