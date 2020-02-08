'''
TODO
'''

import numpy as np

def create_population(params: dict) -> np.ndarray:
    '''
    Generates chromosomes.

    Args:
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Binary chromosomes (population).
    '''

    pop_size = params['algorithm']['populationSize']
    dim_number = _get_dim_number(params)
    chrom_length = _get_length(params)

    population = np.random.randint(2, size=(pop_size, chrom_length*dim_number))

    return population, dim_number, chrom_length

#-------------------------------------------------------------

def _get_dim_number(params: dict) -> int:
    '''
    Gets a number of dimentions for the optimized finction.

    Args:
        params (dict): Algorithm parameters.

    Retuns:
        int: Length of a chromosome.
    '''

    function = params['function']
    dim_number = None

    if function == 1:
        dim_number = 1
    elif function == 2:
        dim_number = 1
    elif function == 3:
        dim_number = 2
    elif function == 4:
        dim_number = 2

    return dim_number

def _get_length(params: dict) -> int:
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
