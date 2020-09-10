import bs4
import re
import requests
from .config import loadControl, loadVersionCheck

def latestVersion():
    """ Extract latest version defined by version-check.json

    Returns
    -------
    version: string
        version extracted from web page
    """
    config = loadVersionCheck()

    content = requests.get(config['url_version']).text.strip()

    if config['html'] is True:
        soup = bs4.BeautifulSoup(content, 'html.parser')
        latest_version = soup.select(config['selector'])[0].contents[0].strip()
    else:
        latest_version = content

    if 'cleaners' in config and len(config['cleaners']) > 0:
        for cleaner in config['cleaners']:
            latest_version = re.sub(cleaner['pattern'], cleaner['rewrite'], latest_version, flags=re.DOTALL).strip()

    return latest_version

def versionChecker(verbose=False):
    """ Compare latest version defined by version-check.json, versus WAPT/control one

    Returns
    -------
    results: bool
        version mismatch
    """
    control = loadControl()
    if verbose:
        print('Current {} version: {}'.format(control['name'], control['version']))

    latest_version = latestVersion()
    if verbose:
        print(' Latest {} version: {}'.format(control['name'], latest_version))

    if control['version'] != latest_version:
        if verbose:
            print('New version available, please upgrade package')

        return True

    return False
