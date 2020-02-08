'''
TODO
'''

import numpy as np

def get_scores(chromosomes: np.ndarray, dim_muber: int, chrom_length: int, params: dict):
    '''
    Assigns fitness to each individual.

    Args:
        chromosomes (np.ndarray): Population.
        dim_number (int): Number of dimensions.
        chrom_length (int): Length of a chromosome.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Fitness values.
    '''

    real_nums = _decode(chromosomes, dim_muber, chrom_length, params)

    fun_values = _get_fun_values(real_nums, params)
    fit_values = _convert_to_fitness(fun_values, params)
    #optimum_value = _get_answer(params['function'])

    return fit_values, real_nums

def get_score(solution: np.ndarray, params: dict):
    '''
    '''

    value = _get_fun_values(solution, params)

    return value

def solved(best_ind: dict, dim_number: int, params: dict):
    '''
    TODO
    '''

    function = params['function']
    precision = float(params['searchDomain']['precision'])

    solution = best_ind['solution']
    solution_found = False

    count = 0
    if function == 4:
        for sln in solution.flatten():
            if _within_range(sln, 1., precision):
                count += 1
    else: # functions 1, 2, 3
        for sln in solution.flatten():
            if _within_range(sln, 0., precision):
                count += 1

    if count == dim_number:
        solution_found = True

    return solution_found

#-------------------------------------------------------------

def _decode(chromosomes: np.ndarray, dim_muber: int, chrom_length: int, params: dict) -> np.ndarray:
    '''
    Decodes genotype (binary representation) to phenotype (real numbers).

    Args:
        chromosomes (np.ndarray): Population.
        dim_number (int): Number of dimensions.
        chrom_length (int): Length of a chromosome.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Real values.
    '''

    phenotype = _binary_to_intereger(chromosomes, dim_muber, chrom_length)
    phenotype = _integer_to_real(phenotype, chrom_length, params)

    return phenotype

def _binary_to_intereger(chromosomes: np.ndarray, dim_muber: int, chrom_length: int) -> np.ndarray:
    '''
    Converts binary strings into integer values.

    Args:
        integers (np.ndarray): Integer numbers.
        dim_number (int): Number of dimensions.
        chrom_length (int): Length of a chromosome.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Integer values.
    '''

    integers = np.zeros((chromosomes.shape[0], dim_muber))
    vector = 2**np.arange(chrom_length)[::-1]

    for i in range(dim_muber):
        integers[:, i] = chromosomes[:, i*chrom_length:(i+1)*chrom_length].dot(vector)

    #integers = chromosomes.dot(2**np.arange(chrom_length)[::-1])
    #integers = chromosomes.dot(1 << np.arange(chrom_length)[::-1]) # faster

    return integers

def _integer_to_real(integers: np.ndarray, chrom_length: int, params: dict) -> np.ndarray:
    '''
    Converts integers to real numbers.

    Args:
        integers (np.ndarray): Integer numbers.
        dim_number (int): Number of dimensions.
        chrom_length (int): Length of a chromosome.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Real values.
    '''

    lower_bound = params['searchDomain']['lowerBound']
    upper_bound = params['searchDomain']['upperBound']

    epsilon = (upper_bound - lower_bound) / (2**chrom_length - 1)
    real_nums = lower_bound + epsilon*integers

    return real_nums

def _get_fun_values(real_nums: np.ndarray, params: dict):
    '''
    Calculates function values.

    Args:
        real_nums (np.ndarray): Real numbers.
        params (dict): Algorithm parameters.

    Returns:
        float: Real optimum value.
    '''

    function = params['function']
    fun_values = None

    if function == 1:
        fun_values = _function_1(real_nums)
    elif function == 2:
        fun_values = _function_2(real_nums)
    elif function == 3:
        fun_values = _function_3(real_nums)
    elif function == 4:
        fun_values = _function_4(real_nums)

    return fun_values.reshape(-1)

def _function_1(real_nums: np.ndarray) -> np.ndarray:
    '''
    Function 1: f(x)=|x|.
    [-10,10], min f(0) = 0.

    Args:
        real_nums (np.ndarray): Real numbers.

    Returns:
        np.ndarray: Function values.
    '''

    fun_values = np.abs(real_nums)

    return fun_values

def _function_2(real_nums: np.ndarray) -> np.ndarray:
    '''
    Function 2. f(x)=-10*cos(x)+|0.001*x|.
    [-10,10], min f(0)=-10.

    Args:
        real_nums (np.ndarray): Real numbers.

    Returns:
        np.ndarray: Function values.
    '''

    fun_values = -10.0*np.cos(real_nums) + np.abs(0.001*real_nums)

    return fun_values

def _function_3(real_nums: np.ndarray) -> np.ndarray:
    '''
    Function 3. Rastrigin function.
    f(x1,x2)=0.1*x1^2+0.1*x2^2-4*cos(0.8*x1)-4*cos(0.8*x2)+8.
    [-16,16], min f(0,0)=0.

    Args:
        real_nums (np.ndarray): Real numbers.

    Returns:
        np.ndarray: Function values.
    '''

    fun_values = 0.1*real_nums[:, 0]**2 + 0.1*real_nums[:, 1]**2 \
        - 4*np.cos(0.8*real_nums[:, 0]) - 4*np.cos(0.8*real_nums[:, 1]) + 8

    return fun_values

def _function_4(real_nums: np.ndarray) -> np.ndarray:
    '''
    Function 4. Rosenbrock function.
    f(x)=100*(x1 - x0^2)^2 + (1-x0)^2.
    [-2;2], min f(1,1)=0.

    Args:
        real_nums (np.ndarray): Real numbers.

    Returns:
        float: Function values.
    '''

    fun_values = 100*(real_nums[:, 1]-real_nums[:, 0]**2)**2 + (1-real_nums[:, 0])**2

    return fun_values

def _convert_to_fitness(fun_values: np.ndarray, params: dict):
    '''
    '''

    function = params['function']
    fit_values = None

    if function == 2: # negative optimum
        fit_values = 1. / (11 + fun_values)
    else: # min=0
        fit_values = 1. / (1 + fun_values)

    return fit_values

def _within_range(x: float, true_x: float, precision: float):
    '''
    '''

    within_range = False

    if (true_x-precision) <= x <= (true_x+precision):
        within_range = True

    return within_range

# def _get_answer(function: int) -> float:
#     '''
#     Gets a real optimum value.

#     Args:
#         function (int): Number of a function being optimized.

#     Returns:
#         float: Real optimum value.
#     '''

#     optimum = None

#     if function == 1:
#         optimum = 0
#     elif function == 2:
#         optimum = 0
#     elif optimum == 3:
#         optimum = 0
#     elif optimum == 4:
#         optimum = 0

#     return optimum
