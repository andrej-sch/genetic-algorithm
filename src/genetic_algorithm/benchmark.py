'''
Benchmark module.
Used for calculating function and fitness values, and checking if the solution is found.
'''

import numpy as np
from genetic_algorithm.utils import square

def get_scores(chromosomes: np.ndarray, dim_num: int, chrom_length: int, params: dict):
    '''
    Assigns fitness to each individual.

    Args:
        chromosomes (np.ndarray): Population.
        dim_num (int): Number of dimensions.
        chrom_length (int): Length of a chromosome.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Fitness values.
    '''

    real_nums = _decode(chromosomes, dim_num, chrom_length, params)()

    fun_values = _get_fun_values(real_nums, params).reshape(-1)
    fit_values = _convert_to_fitness(fun_values, params)

    assert isinstance(fun_values, np.ndarray) 
    assert isinstance(fit_values, np.ndarray)

    return fit_values, real_nums

def get_value(x: np.ndarray, params: dict) -> float:
    '''
    Calculates a function value.

    Args:
        x (np.ndarray): Real value(s) of shape (1, n).
        params (dict): Algorithm parameters.

    Returns:
        float: Function value.
    '''

    # gets ndarray of shape (1,), [0] to acces the element
    return  _get_fun_values(x, params).reshape(-1)[0]

def solved(best_ind: dict, dim_number: int, params: dict):
    '''
    Checks if a solution is found.

    Args:
        best_ind (dict): Best individual.
        dim_number (int): Number of dimensions.
        params (dict): Algorithm parameters.
    '''

    function = params['function']
    precision = float(params['searchDomain']['precision'])
    solution = best_ind['solution']

    if function == 4:
        true_x = 1.0
    else: # functions 1, 2, 3
        true_x = 0.

    count = 0
    for sln in solution.flatten():
        if _within_range(sln, true_x, precision):
            count += 1

    return count == dim_number

#-------------------------------------------------------------

def _decode(chromosomes: np.ndarray, dim_muber: int, chrom_length: int, params: dict) -> np.ndarray:
    '''
    Decodes genotype (binary representation) to phenotype (real numbers).

    Args:
        chromosomes (np.ndarray): Population.
        dim_number (int): Number of dimensions.
        chrom_length (int): Length of a chromosome for one dimension.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Real values.
    '''

    # binary to integers
    integers = np.zeros((chromosomes.shape[0], dim_muber))
    vector = 2**np.arange(chrom_length)[::-1]

    for i in range(dim_muber):
        integers[:, i] = chromosomes[:, i*chrom_length:(i+1)*chrom_length].dot(vector)

    def integer_to_real():

        lower_bound = params['searchDomain']['lowerBound']
        upper_bound = params['searchDomain']['upperBound']

        epsilon = (upper_bound - lower_bound) / (2**chrom_length - 1)
        real_nums = lower_bound + epsilon*integers

        return real_nums

    return integer_to_real

def _get_fun_values(x: np.ndarray, params: dict) -> np.ndarray:
    '''
    Calculates function values.

    Args:
        x (np.ndarray): Real numbers.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Function values.
    '''

    function = params['function']

    if function == 1:
        return _function_1(x)
    elif function == 2:
        return _function_2(x)
    elif function == 3:
        return _function_3(x, square)
    elif function == 4:
        return _function_4(x, square)

    return None # error

def _function_1(x: np.ndarray) -> np.ndarray:
    '''
    Function 1: f(x)=|x|.
    [-10,10], min f(0) = 0.

    Args:
        x (np.ndarray): Real numbers.

    Returns:
        np.ndarray: Function values.
    '''

    return np.abs(x)

def _function_2(x: np.ndarray) -> np.ndarray:
    '''
    Function 2. f(x)=-10*cos(x)+|0.001*x|.
    [-10,10], min f(0)=-10.

    Args:
        x (np.ndarray): Real numbers.

    Returns:
        np.ndarray: Function values.
    '''

    return -10.0*np.cos(x) + np.abs(0.001*x)

def _function_3(x: np.ndarray, sq_term) -> np.ndarray:
    '''
    Function 3. Rastrigin function.
    f(x1,x2)=0.1*x1^2+0.1*x2^2-4*cos(0.8*x1)-4*cos(0.8*x2)+8.
    [-16,16], min f(0,0)=0.

    Args:
        real_nums (np.ndarray): Real numbers.

    Returns:
        np.ndarray: Function values.
    '''

    return 0.1*sq_term(x[:, 0]) + 0.1*sq_term(x[:, 1]) \
           -4*np.cos(0.8*x[:, 0]) - 4*np.cos(0.8*x[:, 1]) + 8

def _function_4(x: np.ndarray, sq_term) -> np.ndarray:
    '''
    Function 4. Rosenbrock function.
    f(x)=100*(x1 - x0^2)^2 + (1-x0)^2.
    [-2;2], min f(1,1)=0.

    Args:
        x (np.ndarray): Real numbers.

    Returns:
        float: Function values.
    '''

    #fun_values = 100*(x[:, 1]-x[:, 0]**2)**2 + (1-x[:, 0])**2
    return 100*sq_term(x[:, 1]-sq_term(x[:, 0])) + sq_term(1-x[:, 0])

def _convert_to_fitness(fun_values: np.ndarray, params: dict) -> np.ndarray:
    '''
    Converts function values into fitness scores.

    Args:
        fun_values (np.ndarray): Function values.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Fitness scores.
    '''

    function = params['function']

    if function == 2: # min=-10
        t = 11
    else: # min=0
        t = 1

    return 1. / (t + fun_values)

def _within_range(x: float, true_x: float, precision: float) -> bool:
    '''
    Check if a value is within a range of given precision.

    Args:
        x (float): Real value to be checked.
        true_x (float): True real value.
        precision (float): Given precision.

    Returns:
        bool: True if the value is within the range.
    '''

    return  (true_x-precision) <= x <= (true_x+precision)
