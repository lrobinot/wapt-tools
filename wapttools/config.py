import json
import os

def loadVersionCheck():
    """ Load version-check.json configuration file

    Returns
    -------
    config: dict
        configuration dictionnary
    """
    with open('version-check.json') as file:
        config = json.load(file)

    return config

def loadControl():
    """ Load WAPT/control configuration file

    This only extract name and version.

    Returns
    -------
    config: dict
        configuration dictionnary
    """
    config = dict()
    with open('WAPT' + os.sep + 'control', 'r') as control:
        for line in control:
            if line.startswith('name'):
                config['name'] = line.split(':')[1].strip()
            if line.startswith('version'):
                config['version'] = line.split(':')[1].split('-')[0].strip()

    return config
