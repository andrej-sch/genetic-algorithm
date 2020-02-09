'''
Utility module.
'''

import yaml
import numpy as np

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