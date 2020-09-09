import bs4
import re
import requests

def latest():
    """ Extract latest version defined by version-check.json

    Returns
    -------
    version: string
        version extracted from web page
    """
    config = config()

    content = requests.get(config['url_version']).text.strip()

    if config['html'] is True:
        soup = bs4.BeautifulSoup(content, 'html.parser')
        latest_version = soup.select(config['selector'])[0].contents[0].strip()
    else:
        latest_version = content

    if len(config['cleaners']) > 0:
        for cleaner in config['cleaners']:
            latest_version = re.sub(cleaner['pattern'], cleaner['rewrite'], latest_version, flags=re.DOTALL).strip()

    return latest_version
