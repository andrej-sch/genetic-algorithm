'''
Genetic algorithm tools.
Used for creating population and perfoming its evolution.
'''

import numpy as np
from scipy.stats import rankdata
from genetic_algorithm.core.utils import roulette_wheel, swap

# number of parents for cossover operation
PARENTS = 2

def create_population(params: dict, dim_number, chrom_length) -> (np.ndarray, int, int):
    '''
    Generates chromosomes.

    Args:
        params (dict): Algorithm parameters.
        dim_number (function): A function getting number of dimensions.
        chrom_length (function): A function getting chromosome's length.

    Returns:
        (np.ndarray, int, int): Binary chromosomes (population),
                                number of dimension, chomosome length per dimension
    '''

    pop_size = params['algorithm']['populationSize']
    dim_num = dim_number(params)
    length = chrom_length(params)

    population = np.random.randint(2, size=(pop_size, length*dim_num))

    return population, dim_num, length

def elitism(chromosomes: np.ndarray, fit_values: np.ndarray, elit_size: int) -> np.ndarray:
    '''
    Perfomrs elitism strategy.

    Args:
        chromosomes (np.ndarray): Current population.
        fit_values (np.ndarray): Fitness values.
        elit_size (int): Number of best individuals to be saved.

    Returns:
        np.ndarray: Best individuals.
    '''

    # select elit_num best individuals
    mask = np.argsort(fit_values)[-elit_size:]
    best_inds = chromosomes[mask, :]

    return best_inds

def selection(fit_values: np.ndarray, params: dict) -> int:
    '''
    Selects a parent for reproduction.

    Args:
        fit_values (np.ndarray): Fitness values.
        params (dict): Algorithm parameters.

    Returns:
        int: Index of a selected parent.
    '''

    sel_type = params['algorithm']['selection']['type']

    if sel_type == 'proportional':
        return _proportional_selection(fit_values, roulette_wheel)
    elif sel_type == 'rank':
        return _rank_selection(fit_values, roulette_wheel)
    elif sel_type == 'tournament':
        tourn_size = params['algorithm']['selection']['tournamentSize']
        return _tournament_selection(fit_values, tourn_size)

    return None

def crossover(chromosomes: np.ndarray, parent1: int, parent2: int, params: dict) -> np.ndarray:
    '''
    Performs crossover between two selected parents.

    Args:
        chromosomes (np.ndarray): Current population.
        parent1 (int): Index of the first parent.
        parent2 (int): Index of the second parent.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Generated chromosome.
    '''

    cross_type = params['algorithm']['crossover']['type']

    if cross_type == 'one-point':
        return _one_point_crossover(chromosomes, parent1, parent2)
    elif cross_type == 'two-point':
        return _two_point_crossover(chromosomes, parent1, parent2, swap)
    elif cross_type == 'uniform':
        return _uniform_crossover(chromosomes, parent1, parent2)

    return None # error

def mutation(chromosomes: np.ndarray, params: dict) -> np.ndarray:
    '''
    Performs mutation over the population.

    Args:
        chromosomes (np.ndarray): Population.
        params (dict): Algorithm parameters.

    Returns:
        np.ndarray: Mutated chromosomes.
    '''

    mut_type = params['algorithm']['mutation']['type']

    if mut_type == 'low':
        return _low_mutation(chromosomes)
    elif mut_type == 'medium':
        return _medium_mutation(chromosomes)
    elif mut_type == 'high':
        return _high_mutation(chromosomes)
    elif mut_type == 'by_value':
        probability = params['algorithm']['mutation']['probability']
        return _mutation(chromosomes, probability)

    return None # error

#-------------------------------------------------------------

def _proportional_selection(fit_values: np.ndarray, roulette_wheel) -> list:
    '''
    Randomly selects a parent proportional to its fitness.

    Args:
        fit_values (np.ndarray): Fitness values.
        roulette_wheel (function): A function randomly selecting an index
                                   proportional to the given cumulative probabilities.

    Returns:
        list: Indeces of selected parent.
    '''

    indeces = []

    # calculate probabilities
    probs = fit_values / fit_values.sum()
    # calculate cumulative probabilities
    cum_probs = probs.cumsum()

    # select two parents
    for _ in range(PARENTS):
        indeces.append(roulette_wheel(cum_probs))

    return indeces

def _rank_selection(fit_values: np.ndarray, roulette_wheel) -> list:
    '''
    Randomly selects a parent proportional to its rank.

    Args:
        fit_values (np.ndarray): Fitness values.
        roulette_wheel (function): A function randomly selecting an index
                                   proportional to the given cumulative probabilities.

    Returns:
        list: Indeces of selected parents.
    '''

    indeces = []

    # lowest value will be ranked as 1
    # highest value will be ranked as n
    # in our case higher value of rank corresponds to a better fitness value.

    # rank fitness values
    ranks = rankdata(fit_values, method='average')
    # calculate probabilities
    probs = ranks / ranks.sum()
    # calculate cumulative probabilities
    cum_probs = probs.cumsum()

    # select two parents
    for _ in range(PARENTS):
        indeces.append(roulette_wheel(cum_probs))

    return indeces

def _tournament_selection(fit_values: np.ndarray, tourn_size: int) -> list:
    '''
    Randomly selects a parent in the tournament.

    Args:
        fit_values (np.ndarray): Fitness values.
        tourn_size (int): Size of the tournament.

    Returns:
        list: Indeces of selected parent.
    '''

    selected = []

    # select two parents
    for _ in range(PARENTS):
        # randomly select parents for the tournament
        indeces = np.arange(fit_values.size)
        mask = np.random.choice(indeces, tourn_size, replace=False)

        # choose the best
        mask_index = np.argmax(fit_values[mask])
        index = mask[mask_index]
        selected.append(index)

    return selected

def _one_point_crossover(chromosomes: np.ndarray, parent1: int, parent2: int) -> np.ndarray:
    '''
    Perfomes one-point crossover.

    Args:
        chromosomes (np.ndarray): Current population.
        parent1 (int): Index of the first parent.
        parent2 (int): Index of the second parent.

    Returns:
        np.ndarray: Generated chromosome.
    '''

    chrom_length = chromosomes.shape[1]

    # randomly select a crossover point, excluding end points
    cp = np.random.randint(1, chrom_length-1)

     # recombination
    child = np.zeros(chrom_length, dtype=int)
    child[:cp] = chromosomes[parent1, :cp]
    child[cp:] = chromosomes[parent2, cp:]

    return child

def _two_point_crossover(chromosomes: np.ndarray, parent1: int, parent2: int, swap) -> np.ndarray:
    '''
    Perfomes two-point crossover.

    Args:
        chromosomes (np.ndarray): Current population.
        parent1 (int): Index of the first parent.
        parent2 (int): Index of the second parent.
        swap (function): Swaps two values if the first one is larger than the second.

    Returns:
        np.ndarray: Generated chromosome.
    '''

    chrom_length = chromosomes.shape[1]

    # randomly select two crossover points
    cp1 = cp2 = 0
    while cp1 == cp2:
        cp1 = np.random.randint(1, chrom_length-1)
        cp2 = np.random.randint(1, chrom_length-1)

    # swap the values if cross_point1 > cross_point2
    cp1, cp2 = swap(cp1, cp2)

    # recombination
    child = np.zeros(chrom_length, dtype=int)
    child[:cp1] = chromosomes[parent1, :cp1]
    child[cp1:cp2] = chromosomes[parent2, cp1:cp2]
    child[cp2:] = chromosomes[parent1, cp2:]

    return child

def _uniform_crossover(chromosomes: np.ndarray, parent1: int, parent2: int) -> np.ndarray:
    '''
    Perfomes uniform crossover.

    Args:
        chromosomes (np.ndarray): Current population.
        parent1 (int): Index of the first parent.
        parent2 (int): Index of the second parent.

    Returns:
        np.ndarray: Generated chromosome.
    '''

    chrom_length = chromosomes.shape[1]

    # create a random mask for parent1 and parent2 for each chromosome gene
    mask = np.random.choice(np.array([parent1, parent2]), size=chrom_length)

    # recombination
    child = np.zeros(chrom_length, dtype=int)
    child[mask == parent1] = chromosomes[parent1, mask == parent1]
    child[mask == parent2] = chromosomes[parent2, mask == parent2]

    return child

def _low_mutation(chromosomes: np.ndarray) -> np.ndarray:
    '''
    Mutates chromosomes.

    Args:
        chromosomes (np.ndarray): Population.

    Retuns:
        np.ndarray: Mutated chromosomes.
    '''

    # generate an array of random numbers within [0,1]
    rand_nums = np.random.uniform(size=chromosomes.shape)
    # define a threshold
    threshold = 1. / (3.*chromosomes.shape[1])
    # set mask
    mask = (rand_nums <= threshold)
    # mutate genes
    chromosomes[mask] = 1 - chromosomes[mask]

    return chromosomes

def _medium_mutation(chromosomes: np.ndarray):
    '''
    Mutates chromosomes.

    Args:
        chromosomes (np.ndarray): Population.

    Retuns:
        np.ndarray: Mutated chromosomes.
    '''

    # generate an array of random numbers within [0,1]
    rand_nums = np.random.uniform(size=chromosomes.shape)
    # define a threshold
    threshold = 1. / chromosomes.shape[1]
    # set mask
    mask = (rand_nums <= threshold)
    # mutate genes
    chromosomes[mask] = 1 - chromosomes[mask]

    return chromosomes

def _high_mutation(chromosomes: np.ndarray):
    '''
    Mutates chromosomes.

    Args:
        chromosomes (np.ndarray): Population.

    Retuns:
        np.ndarray: Mutated chromosomes.
    '''

    # generate an array of random numbers within [0,1]
    rand_nums = np.random.uniform(size=chromosomes.shape)
    # define a threshold
    threshold = 3. / chromosomes.shape[1]
    # set mask
    mask = (rand_nums <= threshold)
    # mutate genes
    chromosomes[mask] = 1 - chromosomes[mask]

    return chromosomes

def _mutation(chromosomes: np.ndarray, probability: float):
    '''
    Mutates chromosomes.

    Args:
        chromosomes (np.ndarray): Population.
        probability (float): Probability of gene's mutation.

    Retuns:
        np.ndarray: Mutated chromosomes.
    '''

    # generate an array of random numbers within [0,1]
    rand_nums = np.random.uniform(size=chromosomes.shape)
    # set mask
    mask = (rand_nums <= probability)
    # mutate genes
    chromosomes[mask] = 1 - chromosomes[mask]

    return chromosomes
