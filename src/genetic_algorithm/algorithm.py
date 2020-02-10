'''
TODO
'''

import argparse
import numpy as np
import matplotlib.pyplot as plt
from utils import read_params, dim_number, chromosome_length
#from encoding import create_population
from tools import create_population, elitism, selection, crossover, mutation
from benchmark import get_scores, get_value, solved

def generation(chromosomes: np.ndarray, fit_values: np.ndarray, params: dict):
    '''
    TODO
    '''

    pop_size = params['algorithm']['populationSize']

    elit_size = 0
    # perform elitism strategy
    if params['algorithm']['elitism']['strategy'] == 'enabled':
        elit_size = params['algorithm']['elitism']['size']
        best_inds = elitism(chromosomes, fit_values, elit_size)

    children = []
    while len(children) < (pop_size-elit_size):

        # perform selection
        parent1, parent2 = selection(fit_values, params)

        # perform crossover
        child = crossover(chromosomes, parent1, parent2, params)

        children.append(child)

    # convert to np.ndarray
    children = np.vstack(children)

    # mutate the new population
    children = mutation(children, params)

    # concatinate with the best individuals
    if elit_size > 0:
        children = np.vstack((children, best_inds))

    # update the population
    chromosomes = children

    return chromosomes

def algorithm(params: dict):
    '''
    TODO
    '''

    iter_num = params['algorithm']['numberOfIterations']

    # best solution ever found
    best_ind = {'fitness':None, 'solution':None, 'value':None}
    solution_found = False

    # stats to display
    max_fit = []
    min_fit = []
    ave_fit = []

    # create population
    chromosomes, dim_num, chrom_length = create_population(params, dim_number, chromosome_length)

    # fitness values
    fit_values, real_nums = get_scores(chromosomes, dim_num, chrom_length, params)

    _set_stats(fit_values, real_nums, best_ind, dim_num, max_fit, min_fit, ave_fit)

    for i in range(iter_num):

        print(f'Generation #{i+1}...')

        chromosomes = generation(chromosomes, fit_values, params)
        fit_values, real_nums = get_scores(chromosomes, dim_num, chrom_length, params)

        # update stats
        _update_stats(fit_values, real_nums, best_ind, dim_num, max_fit, min_fit, ave_fit)

        # check if soultion is found
        if not solution_found:
            solution_found = solved(best_ind, dim_num, params)

            if solution_found:
                best_ind['generation'] = i+1


    _print_stats(best_ind, solution_found)
    _display_plot(max_fit, min_fit, ave_fit, iter_num)

def _set_stats(fit_values: np.ndarray, real_nums: np.ndarray, best_ind: dict,\
               dim_number: int, max_fit: list, min_fit: list, ave_fit: list):
    '''
    '''

    max_value = fit_values.max()
    max_index = np.argmax(fit_values)

    best_ind['fitness'] = max_value
    best_ind['solution'] = real_nums[max_index].reshape(-1, dim_number)
    best_ind['value'] = get_value(best_ind['solution'], params)

    max_fit.append(max_value)
    min_fit.append(fit_values.min())
    ave_fit.append(fit_values.mean())

def _update_stats(fit_values: np.ndarray, real_nums: np.ndarray, best_ind: dict,\
                  dim_number: int, max_fit: list, min_fit: list, ave_fit: list):
    '''
    '''

    max_value = fit_values.max()

    if max_value > best_ind['fitness']:
        max_index = np.argmax(fit_values)
        best_ind['fitness'] = max_value
        best_ind['solution'] = real_nums[max_index].reshape(-1, dim_number)
        best_ind['value'] = get_value(best_ind['solution'], params)

    max_fit.append(max_value)
    min_fit.append(fit_values.min())
    ave_fit.append(fit_values.mean())

def _print_stats(best_ind: dict, solution_found: bool):
    '''
    '''

    print('-'*50)
    if solution_found:
        print('Solution found.')
        print('Generation:', best_ind['generation'])
    else:
        print('Solution not found.')

    solution = best_ind['solution']
    value = best_ind['value']

    for i, sln in enumerate(solution.flatten()):
        print(f'x_{i}: {sln}')

    print('value:', value)
    print('-'*50)

def _display_plot(max_fit: list, min_fit: list, ave_fit: list, iter_num: int):
    '''
    '''

    plt.title("Fitness vs. Number of Generations")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.plot(range(iter_num+1), max_fit, label="Maximum")
    plt.plot(range(iter_num+1), min_fit, label="Minimum")
    plt.plot(range(iter_num+1), ave_fit, label="Average")
    plt.ylim((0, 1.05))
    plt.xticks(np.arange(0, iter_num+1, 2.0))
    plt.legend()
    plt.show()

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
