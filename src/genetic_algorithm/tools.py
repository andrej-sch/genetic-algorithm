'''
TODO
'''

import numpy as np
from scipy.stats import rankdata

def create_population(params: dict, dim_number, chrom_length) -> (np.ndarray, int, int):
    '''
    Generates chromosomes.

    Args:
        params (dict): Algorithm parameters.

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
    parents = None

    if sel_type == 'proportional':
        parents = _proportional_selection(fit_values)
    elif sel_type == 'rank':
        parents = _rank_selection(fit_values)
    elif sel_type == 'tournament':
        tourn_size = params['algorithm']['selection']['tournamentSize']
        parents = _tournament_selection(fit_values, tourn_size)

    return parents

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
        child = _one_point_crossover(chromosomes, parent1, parent2)
    elif cross_type == 'two-point':
        child = _two_point_crossover(chromosomes, parent1, parent2)
    elif cross_type == 'uniform':
        child = _uniform_crossover(chromosomes, parent1, parent2)

    return child

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
        chromosomes = _low_mutation(chromosomes)
    elif mut_type == 'medium':
        chromosomes = _medium_mutation(chromosomes)
    elif mut_type == 'high':
        chromosomes = _high_mutation(chromosomes)
    elif mut_type == 'by_value':
        probability = params['algorithm']['mutation']['probability']
        chromosomes = _mutation(chromosomes, probability)

    return chromosomes

#-------------------------------------------------------------

def _proportional_selection(fit_values: np.ndarray) -> int:
    '''
    Randomly selects a parent proportional to its fitness.

    Args:
        fit_values (np.ndarray): Fitness values.

    Returns:
        int: Index of the chosen parent.
    '''

    indeces = []
    parents = 2

    # calculate probabilities
    probs = fit_values / fit_values.sum()
    # calculate cumulative probabilities
    cumprobs = probs.cumsum()

    # select two parents
    for _ in range(parents):
        r = np.random.uniform()
        for i, prob in enumerate(cumprobs):
            if r <= prob:
                indeces.append(i)
                break

    return indeces

def _rank_selection(fit_values: np.ndarray) -> int:
    '''
    Randomly selects a parent proportional to its rank.

    Args:
        fit_values (np.ndarray): Fitness values.

    Returns:
        int: Index of the chosen parent.
    '''

    indeces = []
    parents = 2

    # lowest value will ranked as 1
    # highest value will be ranked as n
    # in our case higher value of rank corresponds to a better fitness value.

    # rank fitness values
    ranks = rankdata(fit_values, method='average')
    # calculate probabilities
    probs = ranks / ranks.sum()
    # calculate cumulative probabilities
    cumprobs = probs.cumsum()

    # select two parents
    for _ in range(parents):
        r = np.random.uniform()
        for i, prob in enumerate(cumprobs):
            if r <= prob:
                indeces.append(i)
                break

    return indeces

def _tournament_selection(fit_values: np.ndarray, tourn_size: int) -> int:
    '''
    Randomly selects a parent in the tournament.

    Args:
        fit_values (np.ndarray): Fitness values.
        tourn_size (int): Size of the tournament.

    Returns:
        int: Index of the chosen parent.
    '''

    selected = []
    parents = 2

    # select two parents
    for _ in range(parents):
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

def _two_point_crossover(chromosomes: np.ndarray, parent1: int, parent2: int) -> np.ndarray:
    '''
    Perfomes two-point crossover.

    Args:
        chromosomes (np.ndarray): Current population.
        parent1 (int): Index of the first parent.
        parent2 (int): Index of the second parent.

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
    if cp1 > cp2:
        cp1, cp2 = cp2, cp1

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
