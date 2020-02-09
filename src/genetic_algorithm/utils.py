'''
Utility module.
'''

import yaml

def read_parameters(file) -> dict:
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
