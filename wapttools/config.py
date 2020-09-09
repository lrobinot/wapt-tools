import json

def loadcfg():
    """ Extract version-check.json configuration file

    Returns
    -------
    config: dict
        configuration dictionnary
    """
    with open('version-check.json') as file:
        config = json.load(file)

    return config
