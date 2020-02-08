'''
TODO
'''

import yaml

def read_parameters(file):
    '''
    TODO
    '''

    with open(file, 'r') as yaml_file:
        parameters = yaml.full_load(yaml_file)

    return parameters
