import bs4
import json
import re
import requests
import os
from .config import loadControl, loadVersionCheck

chat_message = """
New version of *{package}* have beed detected.

Control version: {old_version}
 Latest version: *{new_version}*

Jump to {homepage}
"""


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
        if 'index' in config:
            index = config['index']
        else:
            index = 0
        latest_version = soup.select(config['selector'])[index].contents[0].strip()
    else:
        latest_version = content

    if 'cleaners' in config and len(config['cleaners']) > 0:
        for cleaner in config['cleaners']:
            latest_version = re.sub(cleaner['pattern'], cleaner['rewrite'], latest_version, flags=re.DOTALL).strip()

    return latest_version


def versionChecker(verbose=False, chat=False):
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

        if chat and 'CHAT_WEBHOOK_URL' in os.environ:
            requests.session().post(
                os.environ['CHAT_WEBHOOK_URL'],
                data=json.dumps({
                    'text': chat_message.format(
                        package=control['name'],
                        old_version=control['version'],
                        new_version=latest_version,
                        homepage=control['homepage'])
                }),
                headers={'Content-Type': 'application/json; charset=UTF-8'}
            )

        return True

    return False
