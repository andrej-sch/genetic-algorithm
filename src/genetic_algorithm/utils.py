'''
Utility module.
'''

import yaml
import numpy as np

swap = lambda x1, x2: (x2, x1) if x1 > x2 else (x1, x2)

square = lambda x: x**2

def read_params(file) -> dict:
    '''
    Read yaml file.

    Args:
        file (str): Path to the yaml file.

    Returns:
        dict: Contents of the yaml file.
    '''

    with open(file, 'r') as yaml_file:
        parameters = yaml.full_load(yaml_file)

    return parameters

def dim_number(params: dict) -> int:
    '''
    Gets a number of dimentions for the optimized finction.

    Args:
        params (dict): Algorithm parameters.

    Retuns:
        int: Length of a chromosome.
    '''

    function = params['function']

    if function == 1:
        return 1
    elif function == 2:
        return 1
    elif function == 3:
        return 2
    elif function == 4:
        return 2

    return None # error

def chromosome_length(params: dict) -> int:
    '''
    Calculates a chromosome's length to be generated.

    Args:
        params (dict): Algorithm parameters.

    Retuns:
        int: Length of a chromosome.
    '''

    lower_bound = params['searchDomain']['lowerBound']
    upper_bound = params['searchDomain']['upperBound']
    precision = float(params['searchDomain']['precision'])

    length = (upper_bound - lower_bound) / precision
    length = int(np.ceil(np.log2(length)))

    return length

def roulette_wheel(cum_probs: np.ndarray) -> int:
    '''
    Randomly selects an index given cumulative probabilities.

    Args:
        cum_probs (np.ndarray): Cumulative probabilities.

    Returns:
        int: Selected index.
    '''

    index = None

    r = np.random.uniform()
    for i, prob in enumerate(cum_probs):
        if r <= prob:
            index = i
            break

    return index


