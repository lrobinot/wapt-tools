import datetime
import os
import sys
from .config import loadControl

def release(package, verbose):
    """ Release package

    Returns
    -------
    results: bool
        version mismatch
    """

    if not os.path.isdir(package):
        if verbose:
            print('*** ERROR: folder {} does not exists, aborting.'.format(package))
        sys.exit(1)

    os.chdir(package)

    control = loadControl()
    version_tag = '{version}-{datetag}'.format(
        version=control['version'],
        datetag=datetime.datetime.now().strftime('%Y%j.%H%M%S'))

    command = 'git flow release start v{tag}'.format(tag=version_tag)
    if verbose:
        print('* {}'.format(command))

    os.system(command)

    command = ('git flow release finish ' + \
        '--push --pushtag --nopushdevelop --nokeep --force_delete ' + \
        '--message "Release v{version} on {date}" v{tag}').format(
            tag=version_tag,
            version=control['version'],
            date=datetime.datetime.now().strftime('%Y-%m-%d, %H:%M'))
    if verbose:
        print('* {}'.format(command))

    os.system(command)
